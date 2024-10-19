from fuzzi_logic import FuzzySet, FuzzyRelation, build_inference

# pressure_surface = [800, 830, 860, 900]
# temperature_surface = [300, 350, 400]
# R1: if the pressure is high, then the temperature is average
# R2: if the pressure is low, then the temperature is low

high_pressure = FuzzySet("800/0.4; 830/0.6; 860/0.8; 900/1")
low_pressure = FuzzySet("800/1; 830/0.9; 860/0.6; 900/0.4")

average_temperature = FuzzySet("300/0.5; 350/1; 400/0.5")
low_temperature = FuzzySet("300/1; 350/0.4; 400/0.1")

relation1 = FuzzyRelation(high_pressure, average_temperature)
relation2 = FuzzyRelation(low_pressure, low_temperature)
relation = relation1.aggregate(relation2)

def read_input_set(surface: list):
    print(f"Input fuzzy set for surface: {set(surface)}.\n"
          f"Try like this: {FuzzySet("'a'/0.1; 'b'/0.2; 'c'/0.3")},\n"
          f"where <a, b, c> items from surface and <0.1, 0.2, 0.3> values of the fuzzy "
          f"set membership function.")
    in_set = input("Enter fuzzy set: ")

    fuzzy_set =  FuzzySet(in_set, surface)
    print("Detected like", fuzzy_set)

    return fuzzy_set

def main():
    print("High pressure:", high_pressure)
    print("Low pressure:", low_pressure)
    print("Average temperature:", average_temperature)
    print("Low temperature:", low_temperature)
    print("\nRelations:\nR1: if the pressure is high, then the temperature is average\n"
          "R2: if the pressure is low, then the temperature is low\n")
    print(f"R1:\n{relation1}\n")
    print(f"R2:\n{relation2}\n")
    print(f"Aggregated relations R:\n{relation}\n")


    in_set = read_input_set(relation.surfaces()[0])
    out_set = build_inference(in_set, relation)

    print(f"\nOutput fuzzy set: {out_set}")


if __name__ == "__main__":
    main()
