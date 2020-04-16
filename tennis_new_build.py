import tkinter as tk
from tkinter import *
import random
import time

window_width = 700
window_height = 400
paddle_width = 10
paddle_height = 80

window = tk.Tk()
window.title('pong')
window.geometry('700x400')
window.resizable(0, 0)
window.wm_attributes('-topmost', 1)
canvas = tk.Canvas(window, width = window_width, height = window_height, background = 'black')
canvas.pack()

ball = canvas.create_oval(355, 195, 365, 205, fill='white', outline='white')
left_paddle = canvas.create_line(paddle_width/2 + 15,
                                 window_height/2 - paddle_height/2,
                                 paddle_width/2 + 15,
                                 window_height/2 + paddle_height/2,
                                 width = paddle_width, fill='white')

right_paddle = canvas.create_line(window_width - paddle_width/2 - 15,
                                  window_height/2 - paddle_height/2,
                                  window_width - paddle_width/2 - 15,
                                  window_height/2 + paddle_height/2,
                                  width = paddle_width, fill='white')

ball_speed = 5
ball_X = [ball_speed, -ball_speed]
ball_Y = [ball_speed, -ball_speed]

random.shuffle(ball_X)
random.shuffle(ball_Y)

ball_X_move = ball_X[0]
ball_Y_move = ball_Y[0]

paddle_speed = 5
left_paddle_speed = 0
right_paddle_speed = 0

left_player_points = 0
right_player_points = 0

score_diff_x = 40
score_diff_y = 20

left_player_score = canvas.create_text(score_diff_x, score_diff_y,
                                       text=left_player_points,
                                       font='Arial 16', fill = 'white')
right_player_score = canvas.create_text(window_width - score_diff_x,
                                        score_diff_y, text=right_player_points,
                                        font='Arial 16', fill = 'white')


def ball_move():
    global ball_X, ball_Y
    canvas.move(ball, ball_X_move, ball_Y_move)
    

def paddle_control():
    paddles = {left_paddle: left_paddle_speed,
               right_paddle: right_paddle_speed}
    for i in paddles:
        canvas.move(i, 0, paddles[i])


canvas.focus_set()

def binds(event):
    global left_paddle_speed, right_paddle_speed, start
    if event.keysym == 'w':
        left_paddle_speed = -paddle_speed
    if event.keysym == 's':
        left_paddle_speed = paddle_speed
    if event.keysym == 'Up':
        right_paddle_speed = -paddle_speed
    if event.keysym == 'Down':
        right_paddle_speed = paddle_speed


canvas.bind('<KeyPress>', binds)



def release(event):
    global left_paddle_speed, right_paddle_speed, start
    if event.keysym == 'w':
        left_paddle_speed = 0
    if event.keysym == 's':
        left_paddle_speed = 0
    if event.keysym == 'Up':
        right_paddle_speed = 0
    if event.keysym == 'Down':
        right_paddle_speed = 0
        
canvas.bind('<KeyRelease>', release)


def left_paddle_stop():
    global left_paddle, left_paddle_speed, window_height
    paddle_pos = canvas.coords(left_paddle)
    l_paddle_top = paddle_pos[1]
    l_paddle_bottom = paddle_pos[3]
    if l_paddle_top <= 0:
        canvas.coords(left_paddle, paddle_width/2 + 15,
                      0, paddle_width/2 + 15, paddle_height)
    if l_paddle_bottom >= window_height:
        canvas.coords(left_paddle, paddle_width/2 + 15,
                      window_height - paddle_height, paddle_width/2 + 15, window_height)


def right_paddle_stop():
    global right_paddle, right_paddle_speed, window_height
    paddle_pos = canvas.coords(right_paddle)
    r_paddle_top = paddle_pos[1]
    r_paddle_bottom = paddle_pos[3]
    if r_paddle_top <= 0:
        canvas.coords(right_paddle, window_width - paddle_width/2 - 15,
                      0, window_width - paddle_width/2 - 15, paddle_height)
    if r_paddle_bottom >= window_height:
        canvas.coords(right_paddle, window_width - paddle_width/2 - 15,
                      window_height - paddle_height, window_width - paddle_width/2 - 15, window_height)



respawn = False
left_scored = False
right_scored = False
whoscored = canvas.create_text(350, 20, font='Arial 20', fill='red')
color = ['blue', 'magenta', 'cyan', 'green', 'red', 'yellow', 'orange', 'pink', 'violet']

def change_move():
    global ball_Y_move, ball_X_move, window_width, window_height, left_paddle, right_paddle
    global left_player_score, left_player_points, right_player_score, right_player_points
    global respawn, fin, left_scored, right_scored, whoscored
    ball_pos = canvas.coords(ball)
    ball_left = ball_pos[0]
    ball_top = ball_pos[1]
    ball_right = ball_pos[2]
    ball_bottom = ball_pos[3]
    ball_center = (ball_top + ball_bottom)/2
    left_paddle_pos = canvas.coords(left_paddle)
    right_paddle_pos = canvas.coords(right_paddle)
    left_paddle_side = left_paddle_pos[0]
    right_paddle_side = right_paddle_pos[0]
    left_paddle_top = left_paddle_pos[1]
    left_paddle_bottom = left_paddle_pos[3]
    right_paddle_top = right_paddle_pos[1]
    right_paddle_bottom = right_paddle_pos[3]
    if ball_top <= 0:
        ball_Y_move = ball_speed
        canvas.itemconfig(whoscored, text='', fill='black')
    if ball_bottom >= window_height:
        ball_Y_move = -ball_speed
        canvas.itemconfig(whoscored, text='', fill='black')
    if ball_left < 0:
        right_player_points += 1
        canvas.itemconfig(right_player_score, text=right_player_points)
        canvas.coords(left_paddle, paddle_width/2 + 15,
                                 window_height/2 - paddle_height/2,
                                 paddle_width/2 + 15,
                                 window_height/2 + paddle_height/2)
        canvas.coords(right_paddle, window_width - paddle_width/2 - 15,
                                  window_height/2 - paddle_height/2,
                                  window_width - paddle_width/2 - 15,
                                  window_height/2 + paddle_height/2)
        right_scored = True
        canvas.coords(ball, 355, 195, 365, 205)
        random.shuffle(color)
        canvas.itemconfig(whoscored, text='Забил второй', fill=color[0])
        respawn = True
    if ball_right > window_width:
        left_player_points += 1
        canvas.itemconfig(left_player_score, text=left_player_points)
        canvas.coords(left_paddle, paddle_width/2 + 15,
                                 window_height/2 - paddle_height/2,
                                 paddle_width/2 + 15,
                                 window_height/2 + paddle_height/2)
        canvas.coords(right_paddle, window_width - paddle_width/2 - 15,
                                  window_height/2 - paddle_height/2,
                                  window_width - paddle_width/2 - 15,
                                  window_height/2 + paddle_height/2)
        left_scored = True
        canvas.coords(ball, 355, 195, 365, 205)
        random.shuffle(color)
        canvas.itemconfig(whoscored, text='Забил первый', fill=color[0])
        respawn = True
    if (ball_left == left_paddle_side) and (left_paddle_top < ball_center < left_paddle_bottom):
        ball_X_move = ball_speed
    if (ball_right == right_paddle_side) and (right_paddle_top < ball_center < right_paddle_bottom):
        ball_X_move = -ball_speed



def spawn():
    global respawn, left_scored, right_scored, whoscored
    if respawn == True:
        if left_scored == True:
            whoscored
        if right_scored == True:
            whoscored
        time.sleep(1)
        respawn = False


itstimetoquit = False

def exit():
    global left_player_points, right_player_points, itstimetoquit
    if left_player_points == 5:
        canvas.create_text(350, 200, text='Выиграл первый!', font='Arial 25', fill='yellow')
        canvas.itemconfig(ball, fill='black', outline='black')
        itstimetoquit = True
    if right_player_points == 5:
        canvas.create_text(350, 200, text='Выиграл второй!', font='Arial 25', fill='yellow')
        canvas.itemconfig(ball, fill='black', outline='black')        
        itstimetoquit = True


def destroy():
    global itstimetoquit
    if itstimetoquit == True:
        sys.exit()

def process():
    ball_move()
    paddle_control()
    change_move()
    left_paddle_stop()
    right_paddle_stop()
    spawn()
    exit()
    destroy()
    window.after(30, process)



process()

window.mainloop()
