import os

import replicate
import logging
from logging_config import configure_logging
import streamlit as st

configure_logging()


@st.cache_resource(show_spinner=False)
def process_image_with_weather(image_url, address, weather_data):
    try:
        rep = replicate.Client(api_token=os.environ.get("llm_api_key"))
        prompt = f"Assume you are creating an entry for your personal journal, if any humans are spotted in the image assume you are one of them and the address where this image was taken is {address} and use the following weather information to explain the day and do not use the numbers from weather data {weather_data}, now describe this image in a narrative way"
        output = rep.run(
            "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
            input={
                "image": f"{image_url}",
                "prompt": prompt
            }
        )
        # The yorickvp/llava-13b model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        sentence = ""
        for item in output:
            # https://replicate.com/yorickvp/llava-13b/api#output-schema
            sentence += f"{item} "
        return sentence
    except Exception as e:
        logging.warning(f"LLM API failed!:\n{e}")
        return "LLM MODEL ERROR: MODEL FAILED!! PLEASE TRY AGAIN AFTER SOMETIME, THANK YOU FOR TRYING OUT THE SYSTEM!!!"
