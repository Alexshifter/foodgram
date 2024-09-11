import json


def fix_template_data(template_data, fix_dict, fix_dict_list):
    pk = 1
    for i in range(len(template_data)):
        fix_dict_list.append(fix_dict.copy())
        fix_dict_list[i].update(pk=pk, fields=template_data[i])
        pk += 1
    return fix_dict_list


with open('ingredients.json', encoding='UTF-8') as file:
    template_data = json.load(file)
fix_dict = {'model': 'recipes.ingredient', 'fields': None}
fix_dict_list = list()
result_dump = fix_template_data(template_data, fix_dict, fix_dict_list)
with open('data_ingr.json', 'w', encoding='UTF-8') as file:
    json.dump(result_dump, file, ensure_ascii=False)
