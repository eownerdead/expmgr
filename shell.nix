{ pkgs ? import <nixpkgs> { }, dev ? false }:
let
  packages = [
    blueprint-compiler
  ] ++ (with pkgs; [
    python3
    meson
    ninja
    pkg-config
    gobject-introspection.dev
    libadwaita.dev
  ]) ++ (with pkgs.python3Packages; [
    pygobject3
    tomlkit
  ]);

  devPackages = [
    blueprint-compiler
    pygobject-stubs
  ] ++ (with pkgs; [
    desktop-file-utils
    mypy
    yapf
  ]) ++ (with pkgs.python3Packages; [
    typeguard
    flake8
    isort
  ]);

  blueprint-compiler = pkgs.python3.pkgs.buildPythonApplication {
    name = "blueprint-compiler";

    src = pkgs.fetchFromGitLab {
      domain = "gitlab.gnome.org";
      owner = "jwestman";
      repo = "blueprint-compiler";
      rev = "e3a37893a8709aa3d6a571ecb5a3f690da0ef82d";
      hash = "sha256-P9Ixbtdz4vcyz7Mpz3QVbXX0+Uy/HsNq8SSe7Fnp5ko=";
    };

    format = "other";

    nativeBuildInputs = with pkgs; [ meson ninja ];
  };

  pygobject-stubs = pkgs.python3Packages.buildPythonPackage rec {
    pname = "pygobject-stubs";
    version = "0.0.8";

    src = pkgs.python3Packages.fetchPypi {
      inherit version;
      pname = "PyGObject-stubs";
      hash = "sha256-Ro1ZsvC+Fb1EgP/+5/pNmy2xpmKD5L3NcQTQAEm43AU=";
    };

    propagatedBuildInputs = with pkgs.python3Packages; [ pygobject3 ];
  };
in
pkgs.mkShell {
  packages = packages ++ pkgs.lib.optional dev devPackages;
}
