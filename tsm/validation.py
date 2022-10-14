

def validate_single_parser(forms):
    if len(forms) == 1:
        form = forms[0]
        if form.is_valid():
            if form.cleaned_data['start_time']:
                form.add_error('start_time', 'Leave empty if just one Parser.')
            if form.cleaned_data['end_time']:
                form.add_error('end_time', 'Leave empty if just one Parser.')
    # if there is one parser there should be no start and end => could be hidden...

def validate_active_parser(forms, c=0):
    count = len(forms)
    max_index = count - 1

    for index, form in enumerate(forms):
        print(index)

        parser = form.cleaned_data
        print(parser)

        if parser['is_active']:
            print("is true")
            c+=1
        if c >1:
            forms[index].add_error('is_active', 'A thing can have just one active parser!')
            break


def check_parser_time_ranges(forms):
    count = len(forms)
    max_index = count - 1

    for index, form in enumerate(forms):

        parser = form.cleaned_data

        next_pos = index + 1
        if next_pos >= count:
            break
        next_parser = forms[next_pos].cleaned_data

        if count > 1:
            if index > 0 and not parser['start_time']:
                forms[index].add_error('start_time', 'Parser must have a Starttime.')
                continue

            if index < max_index and not parser['end_time']:
                forms[index].add_error('end_time', 'Parser must have an Endtime.')
                continue

        if parser['end_time'] != next_parser['start_time']:
            forms[index].add_error('end_time', 'Please check that Parser-Endtime always matches the next Parser-Starttime.')

        if parser['start_time'] and parser['end_time']:
            start = parser['start_time']
            end = parser['end_time']

            if start.strftime('%Y-%m-%d %H:%M') >= end.strftime('%Y-%m-%d %H:%M'):
                forms[index].add_error('end_time', 'Please check that Parser-Endtime is greater than Parser-Starttime.')


def get_number_of_valid_forms(forms):
    count = 0
    for form in forms:
        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
            count += 1
    return count


def check_required_fields(forms, fields):
    for form in forms:
        if form.is_valid():
            form_data = form.cleaned_data
            for field in fields:
                if form_data[field]:
                    continue
                form.add_error(field, 'This field could not be empty.')
