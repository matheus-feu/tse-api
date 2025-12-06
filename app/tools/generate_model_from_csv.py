import keyword
import re
from pathlib import Path

import pandas as pd


def sanititze_column_name(col_name: str) -> str:
    """
    Sanitiza o nome de uma coluna para ser um identificador válido em Python.
    Remove caracteres especiais, espaços e garante que não comece com número
    ou seja uma palavra reservada do Python.
    Args:
        col_name: Nome original da coluna
    Returns:
        Nome sanitizado da coluna
    """

    col_name = col_name.strip().lower()
    col_name = re.sub(r"\s+", "_", col_name)
    col_name = re.sub(r"[^a-z0-9_]", "", col_name)

    if re.match(r'^\d', col_name):
        col_name = f'col_{col_name}'

    if not col_name:
        col_name = 'col'

    if col_name[0].isdigit():
        col_name = f"c_{col_name}"

    if keyword.iskeyword(col_name):
        col_name = f'{col_name}_'

    return col_name


def infer_pg_type(series: pd.Series) -> tuple[str, int | None]:
    """
    Infere tipo PostgreSQL e, para strings, comprimento máximo sugerido.
    Retorna sempre (tipo, length), onde length é usado só para VARCHAR.
    """
    s = series.dropna()

    if s.empty:
        return "TEXT", None

    if pd.api.types.is_integer_dtype(s):
        max_val = s.max()
        min_val = s.min()
        if min_val >= -32768 and max_val <= 32767:
            return "SMALLINT", None
        elif min_val >= -2147483648 and max_val <= 2147483647:
            return "INTEGER", None
        else:
            return "BIGINT", None

    if pd.api.types.is_float_dtype(s):
        return "DOUBLE PRECISION", None

    if pd.api.types.is_bool_dtype(s):
        return "BOOLEAN", None

    try:
        pd.to_datetime(s.head(50), format="%Y-%m-%d %H:%M:%S", errors="raise")
        return "TIMESTAMP", None
    except Exception:
        pass

    max_len = s.astype(str).map(len).max() or 0
    length = min(max_len, 255) if max_len > 0 else 50
    return "VARCHAR", length


def generate_from_csv(
        csv_path: str,
        table_name: str,
        sep: str = ";",
        encoding: str = "latin1",
        sample_rows: int = 5000
):
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path, sep=sep, encoding=encoding, low_memory=False, nrows=sample_rows)

    raw_cols = list(df.columns)
    sanitized_cols = [sanititze_column_name(c) for c in raw_cols]
    inferred = [infer_pg_type(df[c]) for c in raw_cols]

    # CREATE TABLE
    col_defs = []
    for name, (pg_type, length) in zip(sanitized_cols, inferred):
        if pg_type == "VARCHAR" and length:
            col_defs.append(f'    "{name}" VARCHAR({length}) NULL')
        else:
            col_defs.append(f'    "{name}" {pg_type} NULL')

    create_sql = f"CREATE TABLE {table_name} (\n" + ",\n".join(col_defs) + "\n);\n"

    # Model SQLAlchemy
    type_map = {
        "SMALLINT": "SmallInteger",
        "INTEGER": "Integer",
        "BIGINT": "BigInteger",
        "NUMERIC": "Numeric",
        "TEXT": "Text",
        "TIMESTAMP": "DateTime(timezone=True)",
        "DOUBLE PRECISION": "Float",
        "VARCHAR": "String",
        "BOOLEAN": "Boolean",
    }

    model_name = "".join(part.capitalize() for part in table_name.split("_"))

    lines = []
    lines.append("import uuid")
    lines.append("")
    lines.append(
        "from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Numeric, "
        "Text, DateTime, Boolean, String, Float"
    )
    lines.append("from sqlalchemy.dialects.postgresql import UUID")
    lines.append("from app.core.database import Base")
    lines.append("")
    lines.append("")
    lines.append(f"class {model_name}(Base):")
    lines.append(f'    __tablename__ = "{table_name}"')
    lines.append("")
    lines.append("    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)")
    lines.append("")

    for orig, name, (pg_type, length) in zip(raw_cols, sanitized_cols, inferred):
        sa_type = type_map.get(pg_type, "Text")
        if pg_type == "VARCHAR" and length:
            field_type = f"String({length})"
        else:
            field_type = sa_type

        lines.append(f"    {name} = Column({field_type}, nullable=True)")

    model_code = "\n".join(lines)
    return create_sql, model_code, model_name


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Gera SQL e modelo SQLAlchemy a partir de um CSV."
    )
    parser.add_argument("csv_path", nargs="?", help="Caminho para o arquivo CSV")
    parser.add_argument("table_name", nargs="?", help="Nome da tabela a ser criada")
    parser.add_argument(
        "--sep", type=str, default=";", help="Separador do CSV (padrão: ';')"
    )
    parser.add_argument(
        "--encoding", type=str, default="latin1", help="Codificação do CSV"
    )
    parser.add_argument(
        "--output-models-dir",
        type=str,
        default=None,
        help="Diretório para salvar o modelo (ex: app/models)",
    )

    args = parser.parse_args()

    # Se faltou csv_path ou table_name, pergunta no terminal
    if not args.csv_path:
        args.csv_path = input("Informe o caminho do CSV: ").strip()

    if not args.table_name:
        args.table_name = input("Informe o nome da tabela: ").strip()

    if not args.output_models_dir:
        out = input("Diretório para salvar o modelo (ENTER para não salvar): ").strip()
        args.output_models_dir = out or None

    create_sql, model_code, model_name = generate_from_csv(
        csv_path=args.csv_path,
        table_name=args.table_name,
        sep=args.sep,
        encoding=args.encoding,
    )

    suggested_filename = f"{args.table_name}.py".lower()
    print(f"\nSugestão de arquivo para a model: {suggested_filename}")

    if args.output_models_dir:
        out_dir = Path(args.output_models_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / suggested_filename
        out_path.write_text(model_code, encoding="utf-8")
        print(f"\nModelo salvo em: {out_path}")
