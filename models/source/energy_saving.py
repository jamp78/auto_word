from RoundUp import round_up


def energy_saving_cal(ongrid_power, project_capacity, TurbineCapacity, Grade, hours, turbine_numbers,
                      road_length, price):
    ongrid_power = float(ongrid_power) / 10
    print("ongrid_power")
    print(ongrid_power)
    project_capacity = float(project_capacity)
    TurbineCapacity = float(TurbineCapacity)/1000
    Grade = float(Grade)
    hours = float(hours)
    turbine_numbers = float(turbine_numbers)
    road_length = float(road_length)
    price = float(price)
    main_transformer_loss, box_transformer_loss, reactive_compensation, electrical_circuit_loss = 0, 0, 0, 0
    p0, pk = 0, 0
    p0_box = 2.36
    pk_box = 23.2
    if Grade == 110:
        p0 = 43.6
        pk = 232
    else:
        p0 = 50
        pk = 209
    numbers = 1
    if project_capacity <= 30:
        main_transformer_capacity = 0
    elif project_capacity <= 40:
        main_transformer_capacity = 40
    elif project_capacity <= 50:
        main_transformer_capacity = 50
    elif project_capacity <= 63:
        main_transformer_capacity = 63
    elif project_capacity <= 90:
        main_transformer_capacity = 90
    elif project_capacity <= 120:
        main_transformer_capacity = 120
    elif project_capacity <= 150:
        main_transformer_capacity = 150
    elif project_capacity <= 180:
        main_transformer_capacity = 180
    elif project_capacity <= 200:
        main_transformer_capacity = 100
        numbers = 2
    elif project_capacity <= 240:
        main_transformer_capacity = 240
    else:
        main_transformer_capacity = project_capacity
    # box
    if TurbineCapacity <= 2.5:
        box_transformer_capacity = 2.75
    elif TurbineCapacity < 3:
        box_transformer_capacity = 2.9
    elif TurbineCapacity == 3:
        box_transformer_capacity = 3.2
    elif TurbineCapacity <= 3.5:
        box_transformer_capacity = 3.52
    else:
        box_transformer_capacity = TurbineCapacity

    if main_transformer_capacity!=0:
        B = ongrid_power / 2 / main_transformer_capacity / 0.95 / 8000 * 10
        main_transformer_loss = (p0 * 8000 + pk * B * B * hours) / 10000 * numbers

        B = ongrid_power / turbine_numbers / box_transformer_capacity / 0.95 / 8000 * 10
        box_transformer_loss = (p0_box * 8000 + pk_box * B * B * hours) / 10000 * turbine_numbers

        # 无功补偿
        reactive_compensation = main_transformer_capacity * 0.25 * 0.008 * hours / 10
        # 集电线路
        electrical_circuit_loss = 0.005 * hours / 1000 * main_transformer_capacity * \
                                  main_transformer_capacity / 10 * road_length
    # 运行期能耗指标分析
    total_loss = main_transformer_loss + box_transformer_loss + reactive_compensation + electrical_circuit_loss + 105
    coal = round_up(total_loss * 0.32 * 10, 2)
    coal_year = round_up(coal + 6.518, 2)
    print("coal_year")
    print(coal_year)
    gas = 4.43
    unit_energy = round_up(coal_year / ongrid_power*100, 2)
    unit_energy_price = round_up(coal_year / price / ongrid_power * 1000)
    rate_electrical = round_up(total_loss / ongrid_power * 100)

    dict_14_1 = {
        "箱变_容量": box_transformer_capacity*1000,
        "箱变_年耗": round_up(box_transformer_loss, 2),
        "箱变_年耗_占比": round_up(box_transformer_loss / total_loss * 100, 2),
        "集电线路_年耗": round_up(electrical_circuit_loss),
        "集电线路_年耗_占比": round_up(electrical_circuit_loss / total_loss * 100, 2),
        "无功补偿_年耗": round_up(reactive_compensation),
        "无功补偿_年耗_占比": round_up(reactive_compensation / total_loss * 100, 2),
        "主变_年耗": round_up(main_transformer_loss),
        "主变_年耗_占比": round_up(main_transformer_loss / total_loss * 100, 2),
        "站用电_年耗": 105,
        "站用电_年耗_占比": round_up(105 / total_loss * 100, 2),

        "年总用电量": round_up(total_loss, 2),
        "标准煤": coal,
        "年综合能耗": coal_year,
        "单位产品综合能耗": unit_energy,
        "单位产值能耗": unit_energy_price,
        "综合场用电率": rate_electrical,

    }
    return dict_14_1

    # 施工期能耗种类和数量表


def energy_using_cal(sum_EarthStoneBalance_excavation, sum_EarthStoneBalance_back_fill, Concrete_words,
                     Reinforcement):
    sum_EarthStoneBalance_excavation = float(sum_EarthStoneBalance_excavation) / 10000
    sum_EarthStoneBalance_back_fill = float(sum_EarthStoneBalance_back_fill) / 10000
    Concrete_words = float(Concrete_words) / 10000
    Reinforcement = float(Reinforcement)

    # 混凝土
    Concrete_water = round_up(Concrete_words * 0.25 * 10000)
    Concrete_electrical = round_up(Concrete_words * 13.8)
    Concrete_oil = round_up(Concrete_words * 2.8 * 10)
    Concrete_gas = round_up(Concrete_words * 0.15 * 10)

    # 钢筋
    Reinforcement_electrical = round_up(Reinforcement * 119.75 / 10000)
    Reinforcement_oil = round_up(Reinforcement * 0.99 / 1000)
    Reinforcement_gas = round_up(Reinforcement * 3.01 / 1000)

    # 土石方开挖
    sum_EarthStoneBalance_excavation_oil = round_up(sum_EarthStoneBalance_excavation * 0.45 * 10)

    # 土石方回填
    sum_EarthStoneBalance_back_fill_oil = round_up(sum_EarthStoneBalance_back_fill * 0.22 * 10)

    dict_14_2 = {
        "混凝土浇筑_水": Concrete_water,
        "混凝土浇筑_电": Concrete_electrical,
        "混凝土浇筑_柴油": Concrete_oil,
        "混凝土浇筑_汽油": Concrete_gas,
        "钢筋_电": Reinforcement_electrical,
        "钢筋_柴油": Reinforcement_oil,
        "钢筋_汽油": Reinforcement_gas,
        "土石方开挖_柴油": sum_EarthStoneBalance_excavation_oil,
        "土石方回填_柴油": sum_EarthStoneBalance_back_fill_oil,
        "合计_水": round_up(Concrete_water + 8000 + 4800),
        "合计_电": round_up(Concrete_electrical + Reinforcement_electrical+11.68+27.20),
        "合计_柴油": round_up(
            Concrete_oil + Reinforcement_oil + sum_EarthStoneBalance_excavation_oil + sum_EarthStoneBalance_back_fill_oil),
        "合计_汽油": round_up(Concrete_gas + Reinforcement_gas)

    }
    return dict_14_2
