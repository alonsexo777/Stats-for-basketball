import tkinter as tk

def actualizar_label(player, st):
    player["labels"][st].config(text=f"{st}: {player[st]}")

def actualizar_total(equipo):
    for st in equipo['stats']:
        total = sum(player[st] for player in equipo['players'])
        equipo['labels_totales'][st].config(text=f'{st}: {total}')

def change_stat(player, st, cantidad, equipo):
    if player[st] + cantidad < 0:
        return
    
    player[st] += cantidad
    actualizar_label(player, st)
    actualizar_total(equipo)

def crear_equipo(frame, team_name, equipo):
    entrada_equipo = tk.Entry(frame, font=('Arial', 16), justify='center')
    entrada_equipo.insert(0, team_name)
    entrada_equipo.pack (pady=6)





    total_frame = tk.Frame(frame)
    total_frame.pack(pady=6)

    equipo['labels_totales'] = {}

   

    for st in equipo ['stats']:
       label = tk.Label(total_frame, text=f'{st}: 0', width=12)
       label.pack(side='left', padx=6)
       equipo['labels_totales'][st] = label

    for player in equipo['players']:
        player['labels'] = {}

        fila = tk.Frame(frame)
        fila.pack(pady=6)

        enter_name = tk.Entry(fila, width=15)
        enter_name.insert(0, player['name'])
        enter_name.pack(side='left')
        player['enter_name'] = enter_name


        for st in equipo['stats']:
            sub_frame = tk.Frame(fila)
            sub_frame.pack(side='left', padx=6)

            label = tk.Label(sub_frame, text=f'{st}: 0', width=12)
            label.pack()

            player['labels'][st] = label

            buttons = tk.Frame(sub_frame)
            buttons.pack()

            tk.Button(buttons, text='+',
                      command=lambda j=player, s=st: change_stat(j, s, 1, equipo)).pack(side='left',)
            
            tk.Button(buttons, text='-',
                      command=lambda j=player, s=st: change_stat(j, s, -1, equipo)).pack(side='left')
            
root = tk.Tk()
root.title("Basket Stats App")

frame_izq = tk.Frame(root)
frame_izq.pack(side="left", padx=20)

frame_der = tk.Frame(root)
frame_der.pack(side="right", padx=20)

def create_team_data(prefijo):
    return{
        'stats': ['pts', 'reb', 'ast', 'stl', 'blk'],
        'players': [
            {
                'name': f'{prefijo}{i+1}',
                'pts': 0,
                'reb': 0,
                'ast': 0,
                'stl': 0,
                'blk': 0,  
            }
            for i in range(12)
        ]
    }

team_a = create_team_data('A')
team_b = create_team_data('B')

crear_equipo(frame_izq, 'Team A', team_a)
crear_equipo(frame_der, 'Team B', team_b)






root.mainloop()