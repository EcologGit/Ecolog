def group_reports_info_list(reports_info: list) -> dict:

    group_dict = {
                'avg_availability': reports_info[0].get('avg_availability'),
                'avg_beauty': reports_info[0].get('avg_beauty'),
                'avg_purity': reports_info[0].get('avg_purity'),
                'wastes': [],
                }
    
    for dt in reports_info:
        try:
            if dt['results__waste_id__name'] and dt['sum_amount']:
                group_dict['wastes'].append({'waste_type': dt['results__waste_id__name'], 'sum_amount': dt['sum_amount']})
        except KeyError:
            continue
    
    return group_dict