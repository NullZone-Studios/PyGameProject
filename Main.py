import Builder
import Engine

game = Builder.Showcase()
engine = Engine.Engine(game)
game.Build(engine)
engine.Run()