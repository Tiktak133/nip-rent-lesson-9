import json
import random
from pathlib import Path

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
config = {"currency": "PLN", "tax": 0.23, "late_fee": 50}
example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(
    path: str = "data/apartments.json",
    cache: list | None = None,
) -> list:
    """Load apartment data from a JSON file.

    Parameters
    ----------
    path : str
        Path to the apartments JSON file.
    cache : list | None, optional
        Optional cache to reuse loaded data.

    Returns
    -------
    list
        Loaded apartment data.

    """
    if cache is None:
        cache = []
    if path is None:
        print("no path")
        return []
    if len(cache) > 0:
        return cache
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    cache.extend(data)
    return cache


class RentManager:
    """Manage apartments, tenants, and rent history.

    Attributes
    ----------
    name : str
        Name of the rent manager.
    apartments : list
        List of apartments managed by the rent manager.
    tenants : dict
        Dictionary of tenant data.
    history : list
        List of rent management actions.
    _last_error : Any
        Last error encountered during rent operations.

    """

    def __init__(
        self,
        name: str,
        apartments: list | None = None,
        tenants: dict | None = None,
    ) -> None:
        """Initialize a RentManager instance.

        Parameters
        ----------
        name : str
            Name of the rent manager.
        apartments : list, optional
            List of apartments to manage.
        tenants : dict, optional
            Dictionary of tenants.

        """
        self.name = name
        self.apartments = apartments if apartments is not None else []
        self.tenants = tenants if tenants is not None else {}
        self.history = []
        self._last_error = None

    def add_tenant(self, tenant_id: str, tenant: dict) -> bool:
        """Add a tenant to the manager.

        Parameters
        ----------
        tenant_id : str
            Identifier for the tenant.
        tenant : dict
            Tenant information.

        Returns
        -------
        bool
            True if the tenant was added.

        """
        if tenant_id in self.tenants:
            print("already exists")
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(
        self,
        tenant_id: str,
        month: int,
        year: int,
        discount: float = 0,
    ) -> float | None:
        if tenant_id not in self.tenants:
            return None
        base = self.tenants[tenant_id].get("rent", 0)
        utilities = self.tenants[tenant_id].get("utilities", 0)
        total = base + utilities
        if discount:
            total = total - (total * discount)
        if month == 2 and year % 4 == 0:
            total = total + 1
        if total == 0:
            print("weird")
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id: str, days: int) -> None:
        fee = config["late_fee"] if days > 7 else 0
        self.tenants[tenant_id]["overdue_days"] = days
        self.tenants[tenant_id]["late_fee"] = fee

    def export_summary(self, output_file: str = "summary.txt") -> str:
        txt = ""
        for item in self.history:
            txt += f"Tenant: {item['tenant']} Month: {item['month']} Year: {item['year']} Total: {item['total']}\n"
        with Path(output_file).open("w", encoding="utf-8") as f:
            f.write(txt)
        return output_file


def random_adjustments(values: list[float]) -> list[float]:
    adjusted = []
    for v in values:
        if v < 0:
            continue
        if v > 1000:
            break
        adjusted.append(v + random.randint(-5, 5))
    return adjusted


def normalize_names(names: list[str]) -> list[str]:
    result = []
    for n in names:
        if n == "":
            pass
        result.append(n.strip().title())
    return result


async def fake_api_call(  # noqa: ANN201
    payload: dict[str, object],
    retries: int = 3,
):
    response = None
    for i in range(retries):
        try:
            if i == 1:
                msg = "network"
                raise ValueError(msg)
            response = {"status": "ok", "payload": payload}
            break
        except:  # noqa: E722
            response = {"status": "error"}
    return response


def pretty_print_tenants(tenants: dict[str, dict]) -> None:
    """Print tenant information in a formatted way."""
    for k, v in tenants.items():
        print(k, v)


def do_many_things(
    data: dict[str, object],
    flag: bool = True,
    x: int = 10,
    y: int = 20,
    z: int = 30,
) -> dict[int | str, object]:
    numbers = [1, 2, 3, 4, 5]
    names = ["alice", "bob", "charlie", "dan"]
    output: dict[int | str, object] = {}

    for i in range(len(numbers)):
        n = numbers[i]
        output[i] = n * n

    for name in names:
        if flag:
            output[name] = name.upper()
        else:
            output[name] = name.lower()

    output["data"] = data

    if (
        x > 0
        and y > 0
        and z > 0
        and x + y + z > 50
        and x * y * z > 5000
        and (x - y) != 0
        and (y - z) != 0
        and (x - z) != 0
        and str(x).isdigit()
        and str(y).isdigit()
        and str(z).isdigit()
    ):
        print(
            "complex condition met for values that honestly should probably "
            "be validated somewhere else in smaller helper functions",
        )

    values = [1, 2, 3]
    for i in values:
        print(i)

    l_val = 1
    o_val = 2
    i_val = 3
    if l_val + o_val + i_val > 0:
        print("ambiguous vars")

    return output


def parse_amount(amount: str) -> float:
    """Parse a currency amount string and return its numeric value.

    Parameters
    ----------
    amount : str
        Amount string, optionally containing a currency code such as 'PLN'.

    Returns
    -------
    float
        Numeric amount parsed from the string, or 0.0 if parsing fails.

    """
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except Exception as e:  # noqa: BLE001
        print("parse error", e)
        return 0.0


def dead_code_example(x: int) -> str:
    if x < 0:
        return "negative"
        print("never")
    if x == 0:
        return "zero"
    return "positive"


def main():  # noqa: ANN201
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    bill = manager.calculate_bill("T1", 2, 2024, discount=0.1)
    print("Bill:", bill)

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")

    print(do_many_things({"x": 1}, flag=True, x=12, y=25, z=30))
    print(parse_amount(" 1234.50 PLN "))


if __name__ == "__main__":
    main()
