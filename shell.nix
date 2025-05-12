{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
	  python313
	  python313Packages.pygame-ce
	  python313Packages.isort
	  SDL
	  # SDL2_mixer
	  # SDL2_image
	  # SDL2_ttf
	  # SDL2_gfx

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
