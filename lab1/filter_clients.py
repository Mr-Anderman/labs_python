from clients import clients

DISCOUNT = 0.03          # скидка 3 %
REGULAR_FROM = 3         # 3-е обращение для приминения скидки постоянного клиента


def visit_cost(visit, number): #функция подсчета стоимости текущего обращения
    total = 0
    for service, cost in visit:
        if number >= REGULAR_FROM:
            cost = cost * (1 - DISCOUNT)
        total += cost
    return total


def visit_costs(client): #выводит список всех визитов клиента
    return [visit_cost(visit, number)
            for number, visit in enumerate(client["visits"], start=1)]


def average(values): #среднее
    return sum(values) / len(values) if values else 0


def items_count(client): #количество вещей
    return sum(len(visit) for visit in client["visits"])


def print_clients(items):
    print("Фамилия".ljust(10), "Имя".ljust(7),"Отчество".ljust(15), "Телефон".ljust(17),
          "Обращений".ljust(10), "Вещей".ljust(6), "Постоянный".ljust(11),
          "Средний заказ".ljust(14), "Итого")
    for c in items:
        costs = visit_costs(c)
        regular = "да" if len(c["visits"]) >= REGULAR_FROM else "нет"
        print(c["surname"].ljust(10), c["name"].ljust(7),c["middlename"].ljust(15), c["phone"].ljust(17),
              str(len(c["visits"])).ljust(10), str(items_count(c)).ljust(6),
              regular.ljust(11),
              ("%.2f" % average(costs)).ljust(14),
              "%.2f" % sum(costs))


def print_visits(client): #список всех визитов клиента
    print("\n%s %s %s" % (client["surname"], client["name"], client["middlename"]))
    for number, visit in enumerate(client["visits"], start=1):
        note = " (скидка 3 %)" if number >= REGULAR_FROM else ""
        print("  Обращение %d%s:" % (number, note))
        for service, cost in visit:
            if number >= REGULAR_FROM:
                cost = cost * (1 - DISCOUNT)
            print("    " + service.ljust(18), "%.2f" % cost)
        print("    " + "Итого".ljust(18), "%.2f" % visit_cost(visit, number))


def filter_by_average(items, min_average): #фильтр по средней стоимости заказа
    return [c for c in items if average(visit_costs(c)) > min_average]


print("Все клиенты:")
print_clients(clients)
print_visits(clients[0])

min_average = float(input("\nВведите среднюю стоимость заказа: "))
result = filter_by_average(clients, min_average)
if result:
    print("\nКлиенты со средней стоимостью заказа выше", min_average)
    print_clients(result)
else:
    print("Таких клиентов нет")
