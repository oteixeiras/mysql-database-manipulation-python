from faker import Faker
from typing import Any, Optional
import mysql.connector
import random

# Number of records to be created per table
REGISTER_COUNT = 10

"""
    Mandatory fields for each table
"""

STATES_TABLE_FIELDS = "(`name`, `acronym`)"
ADDRESSES_TABLE_FIELDS = "(`state_id`, `street`, `city`, `number`, `cep`)"
CONDOMINIUMS_TABLE_FIELDS = "(`name`,`address_id`)"
BUILDINGS_TABLE_FIELDS = "(`condominium_id`, `color`, `name`)"
PERSONAL_DATA_TABLE_FIELDS = "(`first_name`, `last_name`, `date_of_birth`, `document`)"
OWNERS_TABLE_FIELDS = "(`personal_data_id`)"
TENANTS_TABLE_FIELDS = "(`personal_data_id`, `owner_id`)"
APARTMENTS_TABLE_FIELDS = "(`owner_id`, `building_id`)"
CHANGES_TABLE_FIELDS = "(`due_date`, `value`, `type`, `status`, `apartments_id`)"


"""
    Connection to the database
"""


def create_db_connection(
    user_name: str = "oteixeiras",
    user_password: str = "oteixeiras",
    host_name: str = "localhost",
    database: str = "database_work",
) -> str:
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database,
        )

        print("MySQL Database connection successful")
    except Exception as exc:
        raise exc

    return connection


"""
    Execute actions in database(run querys)
"""


def execute_query(connection: Any, table_name: str, query: str) -> int:
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()

        print(f"Query successful! Table [{table_name}] id created: {cursor.lastrowid}")

        id_generated = cursor.lastrowid

        return id_generated
    except Exception as exc:
        raise exc


"""
    Create query to insert parameterized information
"""


def create_query_input(table_name: str, table_fields: str, data_input: tuple) -> str:
    query = f"""
                INSERT INTO {table_name} {table_fields} VALUES {data_input}
            """

    if table_name == ("owners"):
        query = f"""
                INSERT INTO {table_name} {table_fields} VALUES ({data_input})
            """

    return query


"""
 Create query to delete parameterized information and restart automatic table index increment
"""


def delete_all_data_by_table_name(
    connection: Any,
    name_of_tables: list[str],
    condition: Optional[str] = None,
    reset_auto_increment: bool = True,
) -> str:
    for table_name in name_of_tables:
        query = f"""DELETE FROM {table_name}"""

        if condition:
            query += f"""where {condition}"""

        execute_query(connection=connection, table_name=table_name, query=query)

        if reset_auto_increment:
            reset_query = f"""ALTER TABLE {table_name} AUTO_INCREMENT = 1"""

            execute_query(
                connection=connection,
                table_name=table_name + " Reset increment",
                query=reset_query,
            )


"""
construindo os objetos a serem inseridos no banco
"""


def populate_states_table(connection: Any) -> int:
    table_name = "states"
    states_id_list = []

    states = build_state()

    for state in states:
        value_input = (state["name"], state["acronym"])
        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, STATES_TABLE_FIELDS, value_input),
        )

        if id_generated:
            states_id_list.append(id_generated)

    return len(states_id_list)


def populate_addresses_table(connection: Any) -> int:
    table_name = "addresses"

    addresses_id_list = []
    for _ in range(REGISTER_COUNT):
        address = build_addresse()

        value_input = (
            address["state_id"],
            address["street"],
            address["city"],
            address["number"],
            address["cep"],
        )
        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, ADDRESSES_TABLE_FIELDS, value_input),
        )

        if id_generated:
            addresses_id_list.append(id_generated)

    return len(addresses_id_list)


def populate_condominiums_table(connection: Any, max_addresses_id: int) -> int:
    table_name = "condominiums"

    condominiums_id_list = []
    for _ in range(REGISTER_COUNT):
        condominium = build_condominium(max_addresses_id=max_addresses_id)

        value_input = (condominium["name"], condominium["address_id"])

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(
                table_name, CONDOMINIUMS_TABLE_FIELDS, value_input
            ),
        )

        if id_generated:
            condominiums_id_list.append(id_generated)

    return len(condominiums_id_list)


def populate_buildings_table(connection: Any, max_condominiums_id: int) -> int:
    table_name = "buildings"

    buildings_id_list = []
    for _ in range(REGISTER_COUNT):
        building = build_building(max_condominiums_id=max_condominiums_id)

        value_input = (
            building["condominium_id"],
            building["color"],
            building["name"],
        )

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, BUILDINGS_TABLE_FIELDS, value_input),
        )

        if id_generated:
            buildings_id_list.append(id_generated)

    return len(buildings_id_list)


def populate_personal_data_table(connection: Any) -> int:
    table_name = "personal_data"

    personal_data_id_list = []
    for _ in range(REGISTER_COUNT):
        personal_data = build_personal_data()

        value_input = (
            personal_data["first_name"],
            personal_data["last_name"],
            personal_data["date_of_birth"],
            personal_data["document"],
        )

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(
                table_name, PERSONAL_DATA_TABLE_FIELDS, value_input
            ),
        )

        if id_generated:
            personal_data_id_list.append(id_generated)

    return len(personal_data_id_list)


def populate_owners_table(connection: Any, max_personal_data_id: int) -> int:
    table_name = "owners"

    owners_id_list = []
    for _ in range(REGISTER_COUNT):
        owner = build_owner_data(max_personal_data_id=max_personal_data_id)

        value_input = owner["personal_data_id"]

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, OWNERS_TABLE_FIELDS, value_input),
        )

        if id_generated:
            owners_id_list.append(id_generated)

    return len(owners_id_list)


def populate_tenants_table(
    connection: Any, max_owners_id: int, max_personal_data_id: int
) -> int:
    table_name = "tenants"

    tenants_id_list = []
    for _ in range(REGISTER_COUNT):
        tenant = build_tenant_data(
            max_owners_id=max_owners_id, max_personal_data_id=max_personal_data_id
        )

        value_input = (tenant["personal_data_id"], tenant["owner_id"])

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, TENANTS_TABLE_FIELDS, value_input),
        )

        if id_generated:
            tenants_id_list.append(id_generated)

    return len(tenants_id_list)


def populate_apartments_table(
    connection: Any, max_buildings_id: int, max_owners_id: int
) -> int:
    table_name = "apartments"

    apartments_id_list = []
    for _ in range(REGISTER_COUNT):
        apartment = build_apartment_data(
            max_buildings_id=max_buildings_id, max_owners_id=max_owners_id
        )

        value_input = (apartment["owner_id"], apartment["building_id"])

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, APARTMENTS_TABLE_FIELDS, value_input),
        )

        if id_generated:
            apartments_id_list.append(id_generated)

    return len(apartments_id_list)


def populate_charges_table(connection: Any, max_apartments_id: int) -> int:
    table_name = "charges"

    charges_id_list = []
    for _ in range(REGISTER_COUNT):
        charge = build_charges_data(max_apartments_id=max_apartments_id)

        value_input = (
            charge["due_date"],
            charge["value"],
            charge["type"],
            charge["status"],
            charge["apartments_id"],
        )

        id_generated = execute_query(
            connection=connection,
            table_name=table_name,
            query=create_query_input(table_name, CHANGES_TABLE_FIELDS, value_input),
        )

        if id_generated:
            charges_id_list.append(id_generated)

    return len(charges_id_list)


"""
    Build information for registers
"""


def build_state() -> list[dict]:
    return [
        {"name": "Acre", "acronym": "AC"},
        {"name": "Alagoas", "acronym": "AL"},
        {"name": "Amapá", "acronym": "AP"},
        {"name": "Amazonas", "acronym": "AM"},
        {"name": "Bahia", "acronym": "BA"},
        {"name": "Ceará", "acronym": "CE"},
        {"name": "Espírito Santo", "acronym": "ES"},
        {"name": "Goiás", "acronym": "GO"},
        {"name": "Maranhão", "acronym": "MA"},
        {"name": "Mato Grosso", "acronym": "MT"},
        {"name": "Mato Grosso do Sul", "acronym": "MS"},
        {"name": "Minas Gerais", "acronym": "MG"},
        {"name": "Pará", "acronym": "PA"},
        {"name": "Paraíba", "acronym": "PB"},
        {"name": "Paraná", "acronym": "PR"},
        {"name": "Pernambuco", "acronym": "PE"},
        {"name": "Piauí", "acronym": "PI"},
        {"name": "Rio de Janeiro", "acronym": "RJ"},
        {"name": "Rio Grande do Norte", "acronym": "RN"},
        {"name": "Rio Grande do Sul", "acronym": "RS"},
        {"name": "Rondônia", "acronym": "RO"},
        {"name": "Roraima", "acronym": "RR"},
        {"name": "Santa Catarina", "acronym": "SC"},
        {"name": "São Paulo", "acronym": "SP"},
        {"name": "Sergipe", "acronym": "SE"},
        {"name": "Tocantins", "acronym": "TO"},
    ]


def build_addresse(max_states_id: int = 26) -> dict:
    fake = Faker()

    address = {
        "state_id": random.randint(1, max_states_id),
        "street": fake.street_name(),
        "city": fake.city(),
        "number": fake.building_number(),
        "cep": fake.zipcode(),
    }

    return address


def build_condominium(max_addresses_id: int) -> dict:
    fake = Faker()

    condominium = {
        "name": fake.street_name(),
        "address_id": random.randint(1, max_addresses_id),
    }

    return condominium


def build_building(max_condominiums_id: int) -> dict:
    fake = Faker()

    building = {
        "condominium_id": random.randint(1, max_condominiums_id),
        "color": fake.color(),
        "name": fake.street_name(),
    }

    return building


def build_personal_data() -> dict:
    fake = Faker()

    personal_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": fake.date_of_birth().strftime("%Y-%m-%d"),
        "document": fake.numerify("###########"),  # 11 digits
    }

    return personal_data


def build_owner_data(max_personal_data_id: int) -> dict:
    owner = {
        "personal_data_id": random.randint(1, max_personal_data_id),
    }

    return owner


def build_tenant_data(max_owners_id: int, max_personal_data_id: int) -> dict:
    tenant = {
        "owner_id": random.randint(1, max_owners_id),
        "personal_data_id": random.randint(1, max_personal_data_id),
    }

    return tenant


def build_apartment_data(max_buildings_id: int, max_owners_id: int) -> dict:
    apartment = {
        "owner_id": random.randint(1, max_owners_id),
        "building_id": random.randint(1, max_buildings_id),
    }

    return apartment


def build_charges_data(max_apartments_id: int) -> dict:
    fake = Faker()

    charge = {
        "due_date": fake.date_of_birth().strftime("%Y-%m-%d"),
        "value": fake.random_int(min=10000, max=100000),
        "type": random.choice(change_type()),
        "status": random.choice(change_status()),
        "apartments_id": random.randint(1, max_apartments_id),
    }
    return charge


"""
    Enum of charges table
"""


def change_type() -> list[dict]:
    return ["IPTU", "water", "energy", "condominium"]


def change_status() -> list[dict]:
    return ["paid out", "pending", "late"]


"""
    Insertion flow control
"""


def populate_tables(connection: Any) -> str:
    max_states_id = populate_states_table(connection)

    max_addresses_id = populate_addresses_table(connection)

    max_condominiums_id = populate_condominiums_table(connection, max_addresses_id)

    max_buildings_id = populate_buildings_table(connection, max_condominiums_id)

    max_personal_data_id = populate_personal_data_table(connection)

    max_owners_id = populate_owners_table(connection, max_personal_data_id)

    max_tenants_id = populate_tenants_table(
        connection,
        max_owners_id,
        max_personal_data_id,
    )

    max_apartments_id = populate_apartments_table(
        connection,
        max_buildings_id,
        max_owners_id,
    )

    max_charges_id = populate_charges_table(connection, max_apartments_id)

    total_records = (
        max_states_id
        + max_addresses_id
        + max_condominiums_id
        + max_buildings_id
        + max_personal_data_id
        + max_owners_id
        + max_tenants_id
        + max_apartments_id
        + max_charges_id
    )

    print(f"\nTotal records created in the database: [{total_records}]")


"""
    Start of application
"""


def main() -> str:
    connection = create_db_connection()

    delete_all_data_by_table_name(
        connection=connection,
        name_of_tables=[
            "charges",
            "apartments",
            "tenants",
            "owners",
            "personal_data",
            "buildings",
            "condominiums",
            "addresses",
            "states",
        ],
    )
    populate_tables(connection=connection)


if __name__ == "__main__":
    main()
