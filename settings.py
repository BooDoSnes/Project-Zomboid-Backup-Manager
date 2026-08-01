from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


# Pasta permanente do Windows.
# Isso evita que o PyInstaller --onefile salve as configurações
# dentro da pasta temporária criada a cada execução.
PASTA_DADOS = (
    Path(os.environ.get("APPDATA", Path.home()))
    / "Zomboid Backup Manager"
)
PASTA_CONFIG = PASTA_DADOS / "config"
ARQUIVO_CONFIG = PASTA_CONFIG / "settings.json"

CONFIG_PADRAO = {
    "pasta_saves": str(Path.home() / "Zomboid" / "Saves"),
    "destino_base": str(
        Path.home() / "Desktop" / "Backups Project Zomboid"
    ),
    "max_backups": 2,
    "ultimo_mundo": "",
}


def carregar_configuracoes() -> dict[str, Any]:
    PASTA_CONFIG.mkdir(parents=True, exist_ok=True)

    if not ARQUIVO_CONFIG.exists():
        configuracoes = CONFIG_PADRAO.copy()
        salvar_configuracoes(configuracoes)
        return configuracoes

    try:
        with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        configuracoes = CONFIG_PADRAO.copy()

        # Migração de versões antigas.
        if "destino" in dados and "destino_base" not in dados:
            dados["destino_base"] = dados["destino"]

        configuracoes.update(dados)
        return configuracoes

    except (json.JSONDecodeError, OSError):
        configuracoes = CONFIG_PADRAO.copy()
        salvar_configuracoes(configuracoes)
        return configuracoes


def salvar_configuracoes(configuracoes: dict[str, Any]) -> None:
    PASTA_CONFIG.mkdir(parents=True, exist_ok=True)

    with ARQUIVO_CONFIG.open("w", encoding="utf-8") as arquivo:
        json.dump(
            configuracoes,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )
