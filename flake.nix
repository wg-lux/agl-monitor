{
  description = "A flake providing a Django Server to monitor AGL Network Devices";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
    agl-monitor-repo = {
      url = "github:wg-lux/agl-monitor";
      # Optionally, specify a branch or a specific commit
      # ref = "main";
      # rev = "abc123";
    };

  };

  outputs = { self, nixpkgs, poetry2nix, agl-monitor-repo, ... }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.cudaSupport = false;
        };
        
        pythonEnv = poetry2nix.mkPoetryEnv {
          inherit pkgs;
          src = agl-monitor-repo;
          python = pkgs.python311; # or any other Python version you need
        };
    in
        {
          nixosModules = {
            agl-monitor = { config, pkgs, lib, ... }: {
              options.services.agl-monitor = {
                enable = lib.mkEnableOption "Enable AGL Monitor Server";
                user = lib.mkOption {
                  type = lib.types.str;
                  default = "agl-admin";
                  description = "The user under which the AGL Monitor Server will run";
                };

                group = lib.mkOption {
                  type = lib.types.str;
                  default = "agl-admin";
                  description = "The group under which the AGL Monitor Server will run";
                };

                working-directory = lib.mkOption {
                  type = lib.types.str;
                  #TODO change this to a neutral path
                  default = "/home/agl-admin/agl-monitor";
                  description = "The working directory for the AGL Monitor Server";
                };

                django-secret-key = lib.mkOption {
                  type = lib.types.str;
                  default = "CHANGE_ME";
                  description = "The secret key for the Django application";
                };

                django-debug = lib.mkOption {
                  type = lib.types.bool;
                  default = true;
                  description = "Enable Django debug mode";
                };

                django-settings-module = lib.mkOption {
                  type = lib.types.str;
                  default = "agl_monitor.settings_prod";
                  description = "The settings module for the Django application";
                };

                # Define the port on which the Django server will listen
                port = lib.mkOption {
                  type = lib.types.int;
                  default = 8825;
                  description = "The port on which the Django server will listen";
                };

                # Define the address on which the Django server will listen
                bind = lib.mkOption {
                  type = lib.types.str;
                  default = "172.16.255.4";
                  description = "The address on which the Django server will listen";
                };

                redis-port = lib.mkOption {
                  type = lib.types.int;
                  default = 6449;
                  description = "The port on which the Redis server will listen"; 
                };

                redis-bind = lib.mkOption {
                  type = lib.types.str;
                  default = "127.0.0.1";
                  description = "The address on which the Redis server will listen";
                };

                conf = lib.mkOption {
                  type = lib.types.attrsOf lib.types.any;
                  default = {};
                  description = "Other settings";
                };
              };


            config = lib.mkIf config.services.agl-monitor.enable {
            environment.systemPackages = with pkgs; [
              redis
              libGLU libGL
              glibc
              xorg.libXi xorg.libXmu freeglut
              xorg.libXext xorg.libX11 xorg.libXv xorg.libXrandr zlib
              ncurses5 stdenv.cc binutils
              pythonEnv
            ];

            services.redis.servers."agl-monitor" = {
              enable = true;
              bind = config.services.agl-monitor.redis-bind;
              port = config.services.agl-monitor.redis-port;
              settings = {};
            };

            systemd.services.agl-monitor = {
              description = "AGL Monitor Django Server Service";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];
              serviceConfig = {
                Restart = "always";
                User = config.services.agl-monitor.user;
                Group = config.services.agl-monitor.group;
                WorkingDirectory = "${pkgs.fetchgit {
                  url = "https://github.com/<YourGitHubUsername>/<YourRepoName>";
                  # Optionally, specify a branch or commit
                  # ref = "main";
                  # rev = "abc123";
                }}/agl_monitor";
                Environment = [
                  "PATH=${pythonEnv}/bin:/run/current-system/sw/bin"
                  "LD_LIBRARY_PATH=${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.linuxPackages.nvidia_x11}/lib"
                  "DJANGO_SETTINGS_MODULE=${config.services.agl-monitor.django-settings-module}"
                ];
              };
              script = ''
                export DJANGO_SECRET_KEY=${config.services.agl-monitor.django-secret-key}
                exec gunicorn agl_monitor.wsgi:application --bind ${config.services.agl-monitor.bind}:${toString config.services.agl-monitor.port}
              '';
            };

            systemd.services.agl-monitor-celery = {
              description = "AGL Monitor Django Celery Service";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];
              serviceConfig = {
                Restart = "always";
                User = config.services.agl-monitor.user;
                Group = config.services.agl-monitor.group;
                WorkingDirectory = "${pkgs.fetchgit {
                  url = "https://github.com/<YourGitHubUsername>/<YourRepoName>";
                  # Optionally, specify a branch or commit
                  # ref = "main";
                  # rev = "abc123";
                }}/agl_monitor";
                Environment = [
                  "PATH=${pythonEnv}/bin:/run/current-system/sw/bin"
                  "LD_LIBRARY_PATH=${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.linuxPackages.nvidia_x11}/lib"
                  "DJANGO_SETTINGS_MODULE=${config.services.agl-monitor.django-settings-module}"
                ];
              };
              script = ''
                exec celery -A agl_monitor worker --loglevel=info
              '';
            };

            systemd.services.agl-monitor-celery-beat = {
              description = "AGL Monitor Celery Beat Service";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];
              serviceConfig = {
                Restart = "always";
                User = config.services.agl-monitor.user;
                Group = config.services.agl-monitor.group;
                WorkingDirectory = "${pkgs.fetchgit {
                  url = "https://github.com/<YourGitHubUsername>/<YourRepoName>";
                  # Optionally, specify a branch or commit
                  # ref = "main";
                  # rev = "abc123";
                }}/agl_monitor";
                Environment = [
                  "PATH=${pythonEnv}/bin:/run/current-system/sw/bin"
                  "LD_LIBRARY_PATH=${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.linuxPackages.nvidia_x11}/lib"
                  "DJANGO_SETTINGS_MODULE=${config.services.agl-monitor.django-settings-module}"
                ];
              };
              script = ''
                exec celery -A agl_monitor beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
              '';
            };
          };
        };
      };

      devShell."${system}" = pkgs.mkShell {
            buildInputs = with pkgs; [ 
              poetry
              
              libGLU libGL libgcc gcc
              xorg.libXi xorg.libXmu freeglut
              xorg.libXext xorg.libX11 xorg.libXv xorg.libXrandr zlib 
              ncurses5 stdenv.cc binutils

              python311
              python311Packages.pandas
              python311Packages.numpy

              # Make venv (not very nixy but easy workaround to use current non-nix-packaged python module)
              python3Packages.venvShellHook
            ];

            # Define Environment Variables
            DJANGO_SETTINGS_MODULE="endoreg_home.settings_prod";
            


            # Define Python venv
            venvDir = ".venv";
            postShellHook = ''
             
            '';
          };

    };
}
