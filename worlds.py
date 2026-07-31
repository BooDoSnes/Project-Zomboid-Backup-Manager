from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Mundo:
    identificador: str
    tipo: str
    tipo_label: str
    modo: str
    nome: str
    raiz: Path
    pastas: tuple[str, ...]

    @property
    def nome_exibicao(self) -> str:
        if self.tipo == "multiplayer":
            return self.nome
        return f"{self.modo} • {self.nome}"

    @property
    def pasta_backup(self) -> str:
        texto = f"{self.tipo}_{self.modo}_{self.nome}"
        texto = re.sub(r'[<>:"/\\|?*]+', "_", texto)
        texto = re.sub(r"\s+", "_", texto).strip("._")
        return texto or "mundo"


def detectar_mundos(pasta_saves: Path) -> list[Mundo]:
    mundos: list[Mundo] = []

    if not pasta_saves.is_dir():
        return mundos

    # Single-player: cada modo contém uma ou mais pastas de save.
    for pasta_modo in sorted(pasta_saves.iterdir(), key=lambda p: p.name.lower()):
        if not pasta_modo.is_dir() or pasta_modo.name.lower() == "multiplayer":
            continue

        for pasta_save in sorted(pasta_modo.iterdir(), key=lambda p: p.name.lower()):
            if not pasta_save.is_dir():
                continue

            identificador = f"single|{pasta_modo.name}|{pasta_save.name}"
            mundos.append(
                Mundo(
                    identificador=identificador,
                    tipo="single",
                    tipo_label="Single-player",
                    modo=pasta_modo.name,
                    nome=pasta_save.name,
                    raiz=pasta_modo,
                    pastas=(pasta_save.name,),
                )
            )

    # Multiplayer: associa NomeDoServidor e NomeDoServidor_player.
    pasta_multiplayer = pasta_saves / "Multiplayer"
    if pasta_multiplayer.is_dir():
        diretorios = {
            pasta.name: pasta
            for pasta in pasta_multiplayer.iterdir()
            if pasta.is_dir()
        }

        bases = sorted(
            nome
            for nome in diretorios
            if not nome.endswith("_player")
        )

        for nome in bases:
            pastas = [nome]
            pasta_player = f"{nome}_player"

            if pasta_player in diretorios:
                pastas.append(pasta_player)

            mundos.append(
                Mundo(
                    identificador=f"multiplayer|Multiplayer|{nome}",
                    tipo="multiplayer",
                    tipo_label="Multiplayer",
                    modo="Multiplayer",
                    nome=nome,
                    raiz=pasta_multiplayer,
                    pastas=tuple(pastas),
                )
            )

    return mundos


def filtrar_mundos(mundos: list[Mundo], tipo_label: str) -> list[Mundo]:
    return [
        mundo
        for mundo in mundos
        if mundo.tipo_label == tipo_label
    ]


def encontrar_mundo(
    mundos: list[Mundo],
    identificador: str | None,
) -> Mundo | None:
    if not identificador:
        return None

    return next(
        (
            mundo
            for mundo in mundos
            if mundo.identificador == identificador
        ),
        None,
    )
