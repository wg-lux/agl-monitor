{
  description = "Application for agl-monitor server";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

  };

  outputs = { self, nixpkgs, ... }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        
    in
        {
          # Call with nix develop
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
            DJANGO_SETTINGS_MODULE="agl_monitor.settings_prod";
            


            # Define Python venv
            venvDir = ".venv";
            postShellHook = ''
              # source .venv/bin/activate
              mkdir -p data

              
            '';
          };


        # });
        };
}
