import tkinter as tk
from tkinter import messagebox
import json
import os

# =========================
# MODELOS
# =========================

class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {'pts':0,'reb':0,'ast':0,'stl':0,'blk':0}

class Team:
    def __init__(self, name, prefix):
        self.name = name
        self.players = [Player(f"{prefix}{i+1}") for i in range(12)]

# =========================
# APP
# =========================

class BasketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basket Stats PRO")
        self.root.configure(bg="#121212")

        self.team_a = Team("Team A","A")
        self.team_b = Team("Team B","B")

        self.team_a_color = "#552583"
        self.team_b_color = "#007A33"

        self.time_left = 600
        self.running = False

        self.quarter = 1
        self.max_quarters = 4

        self.build_ui()

    # ================= UI =================

    def build_ui(self):
        top = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        top.pack(fill="x")

        self.score_a = tk.Label(top, text="0", fg="white",
                               bg=self.team_a_color, font=("Arial", 22, "bold"),
                               width=6)
        self.score_a.pack(side="left", padx=20)

        self.quarter_label = tk.Label(top, text="Q1",
                                     fg="white", bg="#444",
                                     font=("Arial", 16, "bold"),
                                     width=4)
        self.quarter_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(top, text="10:00",
                                   fg="white", bg="#333",
                                   font=("Arial", 18))
        self.timer_label.pack(side="left", padx=20)

        self.score_b = tk.Label(top, text="0", fg="white",
                               bg=self.team_b_color, font=("Arial", 22, "bold"),
                               width=6)
        self.score_b.pack(side="left", padx=20)

        controls = tk.Frame(self.root, bg="#121212")
        controls.pack(pady=10)

        self.btn(controls,"Start",self.start_timer).pack(side="left", padx=5)
        self.btn(controls,"Pause",self.pause_timer).pack(side="left", padx=5)
        self.btn(controls,"Reset Time",self.reset_timer).pack(side="left", padx=5)
        self.btn(controls,"Prev Q",self.prev_quarter).pack(side="left", padx=5)
        self.btn(controls,"Next Q",self.next_quarter).pack(side="left", padx=5)
        self.btn(controls,"Guardar",self.save).pack(side="left", padx=5)
        self.btn(controls,"Cargar",self.load).pack(side="left", padx=5)
        self.btn(controls,"MVP",self.show_mvp).pack(side="left", padx=5)

        main = tk.Frame(self.root, bg="#121212")
        main.pack()

        self.frame_a = tk.Frame(main, bg=self.team_a_color, padx=10, pady=10)
        self.frame_a.pack(side="left", padx=10)

        self.frame_b = tk.Frame(main, bg=self.team_b_color, padx=10, pady=10)
        self.frame_b.pack(side="right", padx=10)

        self.build_team(self.frame_a, self.team_a)
        self.build_team(self.frame_b, self.team_b)

    def btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg="#333", fg="white", relief="flat", padx=10)

    def build_team(self, frame, team):
    # Nombre del equipo
     team.entry = tk.Entry(frame, justify="center", font=("Arial", 16, "bold"))
     team.entry.insert(0, team.name)
     team.entry.pack(pady=8, fill="x")

     for i, player in enumerate(team.players):
        card = tk.Frame(frame, bg="#1e1e1e", padx=8, pady=6)
        card.pack(fill="x", pady=3)

        row = tk.Frame(card, bg="#1e1e1e")
        row.pack(fill="x")

        # 🔢 Número jugador
        number = tk.Label(row, text=f"{i+1:02}",
                          fg="#888", bg="#1e1e1e",
                          font=("Arial", 12, "bold"))
        number.pack(side="left", padx=5)

        # 🏷️ Nombre grande tipo ESPN
        name_var = tk.StringVar(value=player.name)

        name_label = tk.Label(row,
                              textvariable=name_var,
                              fg="white",
                              bg="#1e1e1e",
                              font=("Arial", 13, "bold"),
                              anchor="w")
        name_label.pack(side="left", fill="x", expand=True)

        # ✏️ Entrada oculta (para editar)
        name_entry = tk.Entry(row, textvariable=name_var, font=("Arial", 12))
        
        def toggle_edit(e=None, lbl=name_label, ent=name_entry):
            lbl.pack_forget()
            ent.pack(side="left", fill="x", expand=True)
            ent.focus()

        def save_edit(e=None, lbl=name_label, ent=name_entry):
            ent.pack_forget()
            lbl.pack(side="left", fill="x", expand=True)

        name_label.bind("<Double-Button-1>", toggle_edit)
        name_entry.bind("<Return>", save_edit)
        name_entry.bind("<FocusOut>", save_edit)

        player.ui = {
            "name_var": name_var,
            "labels": {}
        }

        # 📊 Stats lado derecho
        stats_frame = tk.Frame(row, bg="#1e1e1e")
        stats_frame.pack(side="right")

        for stat in player.stats:
            sub = tk.Frame(stats_frame, bg="#1e1e1e")
            sub.pack(side="left", padx=3)

            label = tk.Label(sub,
                             text=f"{stat.upper()} 0",
                             fg="white",
                             bg="#1e1e1e",
                             font=("Arial", 10))
            label.pack()

            player.ui["labels"][stat] = label

            btns = tk.Frame(sub, bg="#1e1e1e")
            btns.pack()

            if stat == "pts":
                for v in [1,2,3]:
                    tk.Button(btns, text=f"+{v}",
                              command=lambda p=player,s=stat,val=v:self.change(p,s,val),
                              bg="#444", fg="white", width=2).pack(side="left")
            else:
                tk.Button(btns, text="+",
                          command=lambda p=player,s=stat:self.change(p,s,1),
                          bg="#444", fg="white", width=2).pack(side="left")

            tk.Button(btns, text="-",
                      command=lambda p=player,s=stat:self.change(p,s,-1),
                      bg="#aa3333", fg="white", width=2).pack(side="left")

    # ================= LÓGICA =================

    def change(self, player, stat, val):
        if player.stats[stat] + val < 0:
            return
        player.stats[stat] += val
        player.ui["labels"][stat].config(
            text=f"{stat.upper()}:{player.stats[stat]}")
        self.update_score()

    def update_score(self):
        a = sum(p.stats["pts"] for p in self.team_a.players)
        b = sum(p.stats["pts"] for p in self.team_b.players)

        self.score_a.config(text=a)
        self.score_b.config(text=b)

    # ================= TIMER =================

    def start_timer(self):
        self.running = True
        self.update_timer()

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.time_left = 600
        self.update_timer_label()

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            self.next_quarter()

    def update_timer_label(self):
        m = self.time_left // 60
        s = self.time_left % 60
        self.timer_label.config(text=f"{m:02}:{s:02}")

    # ================= CUARTOS =================

    def update_quarter_label(self):
        self.quarter_label.config(text=f"Q{self.quarter}")

    def next_quarter(self):
        if self.quarter < self.max_quarters:
            self.quarter += 1
        else:
            self.end_game()
            return

        self.reset_timer()
        self.update_quarter_label()

    def prev_quarter(self):
        if self.quarter > 1:
            self.quarter -= 1
            self.reset_timer()
            self.update_quarter_label()

    def end_game(self):
        a = sum(p.stats["pts"] for p in self.team_a.players)
        b = sum(p.stats["pts"] for p in self.team_b.players)

        winner = self.team_a.entry.get() if a > b else self.team_b.entry.get()
        messagebox.showinfo("Final", f"{winner} gana\n{a} - {b}")

    # ================= SAVE / LOAD =================

    def save(self):
        data = {
            "team_a": self.serialize(self.team_a),
            "team_b": self.serialize(self.team_b),
            "quarter": self.quarter,
            "time": self.time_left
        }
        with open("partido.json", "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists("partido.json"):
            return

        with open("partido.json") as f:
            data = json.load(f)

        self.load_team(self.team_a, data["team_a"])
        self.load_team(self.team_b, data["team_b"])

        self.quarter = data["quarter"]
        self.time_left = data["time"]

        self.update_quarter_label()
        self.update_timer_label()
        self.update_score()

    def serialize(self, team):
        return {
            "name": team.entry.get(),
            "players": [
                {"name": p.ui["entry"].get(), "stats": p.stats}
                for p in team.players
            ]
        }

    def load_team(self, team, data):
        team.entry.delete(0, tk.END)
        team.entry.insert(0, data["name"])

        for p, pdata in zip(team.players, data["players"]):
            p.stats = pdata["stats"]
            p.ui["entry"].delete(0, tk.END)
            p.ui["entry"].insert(0, pdata["name"])
            for st in p.stats:
                p.ui["labels"][st].config(text=f"{st}:{p.stats[st]}")

    # ================= MVP =================

    def show_mvp(self):
        players = self.team_a.players + self.team_b.players
        mvp = max(players, key=lambda p: sum(p.stats.values()))
        messagebox.showinfo("MVP", mvp.ui["entry"].get())

    # ================= RESET =================

    def reset_game(self):
        for t in [self.team_a, self.team_b]:
            for p in t.players:
                for st in p.stats:
                    p.stats[st] = 0
                    p.ui["labels"][st].config(text=f"{st}:0")

        self.quarter = 1
        self.update_quarter_label()
        self.reset_timer()
        self.update_score()



# ================= RUN =================

root = tk.Tk()
app = BasketApp(root)
root.mainloop()