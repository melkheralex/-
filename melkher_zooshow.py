class Animal:
    def __init__(self, name, age, weight, habitat, diet):
        self.name = name
        self.age = age
        self.weight = weight
        self.habitat = habitat
        self.diet = diet

    def eat(self):
        return self.name + " кушает свой привычный корм (" + self.diet + ")"

    def sleep(self):
        return self.name + " спит в среде обитания: " + self.habitat


class Reptile(Animal):
    def __init__(self, name, age, weight, habitat, diet, scale_type, is_venomous):
        super().__init__(name, age, weight, habitat, diet)
        self.scale_type = scale_type
        self.is_venomous = is_venomous

    def bask_in_sun(self):
        return self.name + " греется на солнце"

    def shed_skin(self):
        return self.name + " сбрасывает чешую"


class Amphibian(Animal):
    def __init__(self, name, age, weight, habitat, diet, skin_moisture, can_swim):
        super().__init__(name, age, weight, habitat, diet)
        self.skin_moisture = skin_moisture
        self.can_swim = can_swim

    def croak(self):
        return self.name + " громко квакает"

    def regenerate_limb(self):
        return self.name + " регенерирует лапку"


class ZooShow:
    def __init__(self):
        cobra = Reptile("Королевская Кобра Гоша", 5, 6, "Джунгли", "Хищник", "Гладкая чешуя", True)
        croco = Reptile("Крокодил Гена", 12, 200, "Болото", "Хищник", "Твердые щитки", False)
        self.reptiles = [cobra, croco]

        toad = Amphibian("Жаба Клава", 2, 0.3, "Пруд", "Насекомые", 85, True)
        sam = Amphibian("Саламандра Сэм", 3, 0.15, "Лес", "Насекомые", 90, True)
        self.amphibians = [toad, sam]

    def start_booking(self):
        print("--- ДОБРО ПОЖАЛОВАТЬ В НАШ ЗОО-ТЕАТР! ---")
        print("Выберите вид шоу:")
        print("1 — Шоу Пресмыкающихся")
        print("2 — Шоу Земноводных")

        choice = input("Введите номер (1 или 2): ")

        if choice == "1":
            show_name = "ШОУ ПРЕСМЫКАЮЩИХСЯ"
            performers = self.reptiles
            print("\nВы выбрали: " + show_name)
            print("В программе участвуют артисты:")
            for animal in performers:
                print("- " + animal.name + ": " + animal.bask_in_sun() + " и " + animal.shed_skin())

        elif choice == "2":
            show_name = "ШОУ ЗЕМНОВОДНЫХ"
            performers = self.amphibians
            print("\nВы выбрали: " + show_name)
            print("В программе участвуют артисты:")
            for animal in performers:
                print("- " + animal.name + ": " + animal.croak() + " и " + animal.regenerate_limb())

        else:
            print("Неверный выбор категории шоу!")
            return

        print("\nКатегории билетов и цены:")
        print("1 — Стандарт (Обычное место, 5-10 ряд) — 500 сом")
        print("2 — VIP (1-й ряд + фото с артистами) — 1200 сом")

        ticket_choice = input("Выберите тип билета (1 или 2): ")

        if ticket_choice == "1":
            seat_type = "Обычное место (ряд 5-10)"
            price = 500
        elif ticket_choice == "2":
            seat_type = "VIP (1-й ряд, фотосессия включена)"
            price = 1200
        else:
            print("Неверный выбор билета!")
            return

        print("\n" + "-" * 40)
        print("«" + show_name + "»")
        
        if choice == "1":
            print("Они будут делать сальто через огненные кольца, гипнотизировать зрителей и шипеть в такт музыке!")
        else:
            print("Они будут синхронно прыгать по кувшинкам, играть на подводных колокольчиках и делать фокусы с регенерацией!")

        print("\nИнформация о билете:")
        print("Место: " + seat_type)
        print("К оплате: " + str(price) + " сом")
        print("-" * 40)


if __name__ == "__main__":
    show = ZooShow()
    show.start_booking()