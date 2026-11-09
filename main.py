from collections import deque


# =========================
# СВЯЗНЫЙ СПИСОК
# =========================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_all(self):
        elements = []
        current = self.head

        while current:
            elements.append(current.data)
            current = current.next

        return elements


# =========================
# АЛГОРИТМЫ
# =========================

def quick_sort_greenhouses(greenhouses):
    if len(greenhouses) <= 1:
        return greenhouses

    pivot = greenhouses[len(greenhouses) // 2]

    left = [
        g for g in greenhouses
        if g.soil_moisture < pivot.soil_moisture
    ]

    middle = [
        g for g in greenhouses
        if g.soil_moisture == pivot.soil_moisture
    ]

    right = [
        g for g in greenhouses
        if g.soil_moisture > pivot.soil_moisture
    ]

    return (
        quick_sort_greenhouses(left)
        + middle
        + quick_sort_greenhouses(right)
    )


def binary_search_catalog(catalog, target_name):
    low = 0
    high = len(catalog) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_name = catalog[mid][0]

        if mid_name == target_name:
            return catalog[mid]
        elif mid_name < target_name:
            low = mid + 1
        else:
            high = mid - 1

    return None


# =========================
# РАСТЕНИЯ
# =========================

class Crop:
    def __init__(
        self,
        name,
        grow_days,
        optimal_temp,
        water_need,
        yield_rate
    ):
        self.name = name
        self.grow_days = grow_days
        self.optimal_temp = optimal_temp
        self.water_need = water_need
        self.yield_rate = yield_rate


# =========================
# СКЛАД
# =========================

class Warehouse:
    def __init__(self):
        self.storage = {
            "вода": 500,
            "энергия": 300,
            "удобрения": 100,
            "Томаты": 0,
            "Огурцы": 0,
            "Зелень": 0,
            "Перец": 0
        }

    def add(self, item, amount):
        self.storage[item] = (
            self.storage.get(item, 0) + amount
        )

    def take(self, item, amount):
        if amount < 0:
            return False

        if self.storage.get(item, 0) >= amount:
            self.storage[item] -= amount
            return True

        return False

    def has(self, item, amount):
        return self.storage.get(item, 0) >= amount


# =========================
# КЛИМАТИЧЕСКАЯ СИСТЕМА
# =========================

class ClimateSystem:
    def __init__(self, name):
        self.name = name
        self.wear = 0

    def work(self, warehouse, energy_cost):
        if self.wear >= 100:
            return False

        if not warehouse.take("энергия", energy_cost):
            return False

        self.wear = min(100, self.wear + 5)
        return True

    def regulate(self, greenhouse, warehouse):
        if greenhouse.crop is None:
            return

        target = greenhouse.crop.optimal_temp
        current = greenhouse.temperature

        if current == target or self.wear >= 100:
            return

        if not warehouse.take("энергия", 2):
            return

        if current < target:
            greenhouse.temperature += 1
        else:
            greenhouse.temperature -= 1

        self.wear = min(100, self.wear + 1)


# =========================
# ТЕПЛИЦА
# =========================

class GreenHouse:
    def __init__(self, gh_id, area):
        self.gh_id = gh_id
        self.area = area
        self.status = "пусто"
        self.crop = None
        self.days_growing = 0
        self.temperature = 20
        self.soil_moisture = 60
        self.history = LinkedList()
        self.climate_system = ClimateSystem(
            f"Климат-контроль {gh_id}"
        )


# =========================
# ЯДРО СИМУЛЯЦИИ
# =========================

class GreenHouseSimulation:
    def __init__(self):
        self.day = 1
        self.budget = 100000
        self.warehouse = Warehouse()

        self.greenhouses = [
            GreenHouse("Теплица_1", 50),
            GreenHouse("Теплица_2", 40),
            GreenHouse("Теплица_3", 30),
            GreenHouse("Теплица_4", 35)
        ]

        self.task_queue = deque()

        self.catalog = sorted([
            ("Томаты", 7, 24, 15, 8),
            ("Огурцы", 5, 22, 20, 10),
            ("Зелень", 3, 18, 10, 4),
            ("Перец", 8, 25, 12, 6)
        ])

    def find_greenhouse(self, gh_id):
        return next(
            (g for g in self.greenhouses if g.gh_id == gh_id),
            None
        )

    def show_status(self):
        print(
            f"\n=== ДЕНЬ {self.day} | "
            f"Бюджет: {self.budget} руб. ==="
        )

        print("\nСклад:")
        for item, amount in self.warehouse.storage.items():
            print(f"  {item}: {amount}")

        print("\nТеплицы (от самых сухих к влажным):")

        sorted_gh = quick_sort_greenhouses(self.greenhouses)

        for g in sorted_gh:
            crop_name = g.crop.name if g.crop else "нет"

            print(
                f"\n[{g.gh_id}]"
                f"\nПлощадь: {g.area} м²"
                f"\nСтатус: {g.status}"
                f"\nКультура: {crop_name}"
                f"\nТемпература: {g.temperature}°C"
                f"\nВлажность: {g.soil_moisture}%"
                f"\nРост: {g.days_growing} дней"
                f"\nИзнос оборудования: "
                f"{g.climate_system.wear}%"
            )

        print(f"\nЗадач в очереди: {len(self.task_queue)}")

    # ---------- ПОСТАНОВКА ЗАДАЧ ----------

    def add_task(self):
        print("\nВарианты работ:")
        print("1 — Посев")
        print("2 — Полив")
        print("3 — Сбор урожая")

        choice = input("Номер операции: ").strip()

        if choice not in ["1", "2", "3"]:
            print("[!] Неверный код операции.")
            return

        gh_id = input("Идентификатор теплицы: ").strip()
        greenhouse = self.find_greenhouse(gh_id)

        if greenhouse is None:
            print(f"[!] Теплица '{gh_id}' отсутствует.")
            return

        # --- ПОСЕВ ---
        if choice == "1":
            if greenhouse.status != "пусто":
                print("[!] Теплица уже используется.")
                return

            crop_name = input(
                "Наименование культуры: "
            ).strip().capitalize()

            if binary_search_catalog(self.catalog, crop_name) is None:
                print("[!] Культура не найдена.")
                return

            if any(
                task["gh_id"] == gh_id and task["type"] == "plant"
                for task in self.task_queue
            ):
                print("[!] Посев для этой теплицы уже в очереди.")
                return

            self.task_queue.append({
                "type": "plant",
                "gh_id": gh_id,
                "crop": crop_name
            })
            print(f"[+] Посев {crop_name} добавлен в очередь.")

        # --- ПОЛИВ ---
        elif choice == "2":
            if greenhouse.status not in ["засеяно", "созрело"]:
                print("[!] Поливать можно только занятую теплицу.")
                return

            if greenhouse.soil_moisture >= 90:
                print("[!] Почва достаточно увлажнена.")
                return

            if any(
                task["gh_id"] == gh_id and task["type"] == "water"
                for task in self.task_queue
            ):
                print("[!] Полив для этой теплицы уже в очереди.")
                return

            self.task_queue.append({
                "type": "water",
                "gh_id": gh_id
            })
            print("[+] Полив добавлен в очередь.")

        # --- СБОР ---
        elif choice == "3":
            if greenhouse.status != "созрело":
                print("[!] Урожай еще не готов.")
                return

            if any(
                task["gh_id"] == gh_id and task["type"] == "harvest"
                for task in self.task_queue
            ):
                print("[!] Сбор для этой теплицы уже в очереди.")
                return

            self.task_queue.append({
                "type": "harvest",
                "gh_id": gh_id
            })
            print("[+] Уборка добавлена в очередь.")

    # ---------- ИСПОЛНЕНИЕ ЗАДАЧ ----------

    def plant_crop(self, greenhouse, crop_name):
        if greenhouse.status != "пусто":
            print("[!] Посев отменен: теплица занята.")
            return

        catalog_item = binary_search_catalog(self.catalog, crop_name)
        if catalog_item is None:
            print("[!] Культура отсутствует в справочнике.")
            return

        seed_cost = 500
        energy_cost = 10

        if self.budget < seed_cost:
            print("[!] Недостаточно денег для посева.")
            return

        if not greenhouse.climate_system.work(
            self.warehouse, energy_cost
        ):
            print("[!] Недостаточно энергии или оборудование неисправно.")
            return

        self.budget -= seed_cost
        greenhouse.crop = Crop(
            catalog_item[0],
            catalog_item[1],
            catalog_item[2],
            catalog_item[3],
            catalog_item[4]
        )
        greenhouse.status = "засеяно"
        greenhouse.days_growing = 0

        greenhouse.history.append(
            f"День {self.day}: Посев {crop_name}"
        )
        print(f"[+] {greenhouse.gh_id}: посев {crop_name} выполнен.")

    def water_crop(self, greenhouse):
        # Полив разрешён и для растущей, и для созревшей культуры.
        if greenhouse.status not in ["засеяно", "созрело"] or greenhouse.crop is None:
            print("[!] Полив отменен: в теплице нет культуры.")
            return

        if greenhouse.soil_moisture >= 90:
            print("[!] Полив отменен: почва достаточно влажная.")
            return

        water_needed = greenhouse.crop.water_need

        if not self.warehouse.take("вода", water_needed):
            print("[!] Недостаточно воды.")
            return

        greenhouse.soil_moisture = min(
            100, greenhouse.soil_moisture + 25
        )
        greenhouse.history.append(
            f"День {self.day}: Полив ({water_needed} л)"
        )
        print(f"[+] {greenhouse.gh_id} полита.")

    def harvest_crop(self, greenhouse):
        if greenhouse.status != "созрело" or greenhouse.crop is None:
            print("[!] Сбор отменен: урожай не готов.")
            return

        if not greenhouse.climate_system.work(
            self.warehouse, 15
        ):
            print("[!] Недостаточно энергии или оборудование неисправно.")
            return

        crop = greenhouse.crop
        yield_amount = greenhouse.area * crop.yield_rate
        revenue = yield_amount * 200

        self.warehouse.add(crop.name, yield_amount)
        self.budget += revenue

        greenhouse.history.append(
            f"День {self.day}: Сбор {yield_amount} кг "
            f"{crop.name} (выручка {revenue} руб.)"
        )

        greenhouse.status = "пусто"
        greenhouse.crop = None
        greenhouse.days_growing = 0
        greenhouse.soil_moisture = 60

        print(
            f"[+] Урожай с {greenhouse.gh_id} собран: "
            f"{yield_amount} кг."
        )
        print(f"[+] Выручка: {revenue} руб.")

    def process_tasks(self):
        while self.task_queue:
            task = self.task_queue.popleft()
            greenhouse = self.find_greenhouse(task["gh_id"])

            if greenhouse is None:
                continue

            if task["type"] == "plant":
                self.plant_crop(greenhouse, task["crop"])
            elif task["type"] == "water":
                self.water_crop(greenhouse)
            elif task["type"] == "harvest":
                self.harvest_crop(greenhouse)

    # ---------- ТЕЧЕНИЕ ВРЕМЕНИ ----------

    def update_greenhouses(self):
        for greenhouse in self.greenhouses:
            if greenhouse.status != "засеяно" or greenhouse.crop is None:
                continue

            # Ежедневное испарение влаги.
            greenhouse.soil_moisture = max(
                0, greenhouse.soil_moisture - 5
            )

            # Гибель культуры при полной засухе.
            if greenhouse.soil_moisture == 0:
                greenhouse.history.append(
                    f"День {self.day}: Культура "
                    f"{greenhouse.crop.name} погибла из-за засухи!"
                )
                print(
                    f"[!] {greenhouse.gh_id}: "
                    f"{greenhouse.crop.name} погибли от засухи!"
                )
                greenhouse.status = "пусто"
                greenhouse.crop = None
                greenhouse.days_growing = 0
                greenhouse.soil_moisture = 60
                continue

            # Автоматическая корректировка температуры.
            greenhouse.climate_system.regulate(
                greenhouse, self.warehouse
            )

            temperature_difference = abs(
                greenhouse.temperature -
                greenhouse.crop.optimal_temp
            )

            if temperature_difference <= 5:
                greenhouse.days_growing += 1
            else:
                greenhouse.days_growing += 0.5

            if greenhouse.days_growing >= greenhouse.crop.grow_days:
                greenhouse.status = "созрело"
                greenhouse.history.append(
                    f"День {self.day}: Культура созрела!"
                )
                print(
                    f"[+] {greenhouse.gh_id}: "
                    f"{greenhouse.crop.name} созрели."
                )

    def next_day(self):
        self.day += 1
        print(f"\n========== ДЕНЬ {self.day} ==========")

        # 1. Растём и стареем.
        self.update_greenhouses()

        # 2. Выполняем запланированные действия.
        print("\n--- Исполнение поручений ---")
        self.process_tasks()

        print("\n[+] Сутки обработаны.")

    def show_history(self):
        gh_id = input("Идентификатор теплицы: ").strip()
        greenhouse = self.find_greenhouse(gh_id)

        if greenhouse is None:
            print("[!] Теплица не найдена.")
            return

        print(f"\nИстория {gh_id}:")
        history = greenhouse.history.get_all()

        if not history:
            print("История пока пуста.")
            return

        for event in history:
            print(" •", event)

    # ---------- ГЛАВНЫЙ ЦИКЛ ----------

    def run(self):
        print("\n====================================")
        print("   СИМУЛЯТОР УМНОЙ ТЕПЛИЦЫ")
        print("====================================")

        while True:
            self.show_status()

            print("\nМеню:")
            print("1 — Новая задача")
            print("2 — Следующий день")
            print("3 — История теплицы")
            print("0 — Выход")

            cmd = input("\nВыбор: ").strip()

            if cmd == "1":
                self.add_task()
            elif cmd == "2":
                self.next_day()
            elif cmd == "3":
                self.show_history()
            elif cmd == "0":
                print("\nЗавершение симуляции.")
                break
            else:
                print("[!] Неизвестная команда.")


if __name__ == "__main__":
    game = GreenHouseSimulation()
    game.run()
