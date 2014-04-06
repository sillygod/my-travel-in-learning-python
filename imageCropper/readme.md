# Environment: python 3.2 , pygame


Intention:

 - learn pygame and be familiar with it
 - due to pygame has nothing about gui widgets, I need to implement them myself.
 - now, everything is just a test..

structure:

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

