def checkAvailability(day, ride ):
    new_time_slots = ['9:00-11:00','11:00-12:00','14:00-15:00','15:00-17:00']


    if day == 2:
        new_time_slots.remove('9:00-11:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('14:00-15:00')
    if day == 3:
        if ride == '2T':
            new_time_slots.remove('14:00-15:00')
            new_time_slots.remove('11:00-12:00')
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
    if day == 4:
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('15:00-17:00')
    if day == 5:
        new_time_slots.remove('14:00-15:00')
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
    if day == 6:
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('15:00-17:00')
    if day == 7:
        new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
    if day == 1:
        new_time_slots.remove('15:00-17:00')
        if ride == 'FT':
            new_time_slots.remove('9:00-11:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')