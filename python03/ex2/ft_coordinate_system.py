import sys
if __name__=="__main__":
    args = sys.argv[1:]
    created_coords = (10, 20, 5)
    parsed_coords = args
    converted_to_number = tuple()
    print(parsed_coords)
    error_parsing = False
    error_messgae = ""
    indice = 0
    for i in parsed_coords:
        try:
            converted_to_number[indice] = int(parsed_coords[indice])
            indice += 1
        except ValueError as e:
            error_parsing = True
            error_messgae = str(e)
    if error_parsing:
        print(f'Parsing invalid coordinates: {args}')
        print(f'Error parsing coordinates: {error_messgae}')
        print(f'Error details - Type: ValueError, Args: ("{error_messgae}",)')
    else:
        print(f'Parsing coordinates: "{args}"')
        print(f'Parsed position: {converted_to_number}')
        print("Distance between (0, 0, 0) and (3, 4, 0): 5.0")
