module Main exposing (main)

import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)
import Time exposing (Month)

main : Program () Model Msg
main =
  Browser.sandbox { init = init, update = update, view = view }

type Msg = Increment | Decrement

type alias Model = { count : Int, month : Month, year: Int }
init = { count = 0, month = Time.Dec, year = 2024 }

update : Msg -> Model -> Model
update msg model =
    case msg of
        Increment ->
            { model | count = model.count + 1 }

        Decrement ->
             { model | count = model.count - 1 }

view : Model -> Html Msg
view model =
    div []
        [ button [onClick Decrement] [ text "-"]
        , div [] [text (String.fromInt model.count)]
        , button [onClick Increment] [text "+"]
        ]

type alias Day = {day: Int, month: Month, year: Int}

firstMondayBefore : Model -> Day
firstMondayBefore model =
    -- get a Posix time for the first day of the month
    let
        now = Time.now
        otherNow = 
