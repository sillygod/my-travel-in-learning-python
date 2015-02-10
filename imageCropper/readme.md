`Environment: python 3.2 , pygame`


# Intention

 - learn pygame and be familiar with it
 - due to pygame has nothing about gui widgets, I need to implement them myself.
 - now, everything is just a test..

# structure

 - class App

    the main game control flow

 - class Action

    bind function and pygame event

 - class Controller

    responsible for the pygame event control

 - class render

    accept a pygame surface which is the central part for how to arrange the widget

 - class widget

    basic class for gui element

 - class Button

    can bind key or mouse click

 - class Label

    show a brief string



# preview

![preview](http://i.imgur.com/UZ5Ik41.png)


#think note

```
maybe, it should have an object for the layout of all widget.
a need for coordinate system?
try to add more widget. ex. listbox, scrollbar

a class responsible for font's size and position


```

