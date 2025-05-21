# Examples

This repository features a growing collection of example projects built with Kdeps, including:

## **tools**
An API that allows LLM to autonomously choose a tool to execute (like MCP, A2A). There is 2 python tools that are exposed to LLM in the `data/` folder. This example uses the `llama3.2` model.

```shell
curl 'http://localhost:3000/api/v1/tools'
```

Output:

```json
{
  "meta": {
    "requestID": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"
  },
  "response": {
    "data": [
      {
        "final_value": "10019",
        "number_of_tools_used": 2
      }
    ]
  },
  "success": true
}
```

## **vision**
An API that uses LLM Vision model. It accepts the prompt via a param `q`. This example uses `moondream:1.8b` vision model.
NOTE: If you need to specify `JSONResponseKeys`, please use a more capable model. i.e. llama.

```shell
curl 'http://localhost:3000/api/v1/vision?q=What%20is%20this%20image?' -X POST -F "file[]=@assets/redpanda_small.png"
```

Output:

```json
{
  "meta": {
    "requestID": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"
  },
  "response": {
    "data": [
      "The image features a small red panda sitting on the ground, holding a pink balloon with its paws. The panda appears to be enjoying itself as it holds onto the balloon, which is positioned above its head."
    ]
  },
  "success": true
}
```

## **ai_ocr_api**
An API that combines Tesseract (images) or Poppler-utils (PDF) and LLM to create a JSON response. To interact with the API using
`curl`, run:

```shell
curl 'http://localhost:3000/api/v1/ocr' -X POST -F "file[]=@assets/testocr.png"
```

And outputs:

```json
{
  "errors": null,
  "response": {
    "data": [
      {
        "document_category": "Sample Text",
        "document_description": "Testing OCR code with a sample text document.",
        "document_text_array": [
          "This is a lot of 12 point text to test the ocr code and see if it works on all types of file format.",
          "The quick brown dog jumped over the lazy fox. The quick brown dog jumped over the lazy fox. The quick brown dog jumped over the lazy fox. The quick brown dog jumped over the lazy fox."
        ],
        "document_type": "Text Document"
      }
    ]
  },
  "success": true
}
```

This is the test image:

![OCR test image](/assets/testocr.png)

## **weather_forecast_api**
A Weather Forecast API that connects to an external provider (https://open-meteo.com) to fetch weather data. It uses
request parameters to pass input values. To interact with the API using `curl`, run:

```shell
curl "http://localhost:3000/api/v1/forecaster?q=What+is+the+weather+in+Amsterdam?"
```

And outputs:

```json
{
  "errors": [
    {
      "code": 0,
      "message": ""
    }
  ],
  "response": {
    "data": [
      {
        "activities": "If you're looking for something to do in Amsterdam today, consider checking out local concerts or festivals that are happening indoors since it's mostly cloudy outside. The weather isn't too bad, but it's not ideal for outdoor activities either. You could also visit some of the city's museums or indoor shopping malls to stay warm and dry.\n\nIf you're up for a hike, there are still some great trails in Amsterdam that can handle light winds and cool temperatures like today's. The city has plenty of parks and gardens where you can enjoy the scenery without getting too wet. Some popular options include the Vondelpark or the Amsterdamse Bos. Just be sure to dress warmly and wear layers.\n\nFor tomorrow, it looks like the weather will be a bit warmer, with highs reaching 2°C. If you're planning on spending time outdoors, consider visiting some of the city's gardens or parks that are designed for walking and exploring. The Hortus Botanicus is a great option, featuring a variety of plant species from around the world. Alternatively, you could check out one of the many indoor venues in Amsterdam, such as the Rijksmuseum or the Van Gogh Museum.",
        "dining_recommendations": "If you're looking for some comfort food to warm you up on a chilly day in Amsterdam, consider visiting restaurants like De Kas or Bauta. They offer hearty meals that are perfect for cold weather, such as stews and soups. Another option is Guts \u0026 Glory, which serves seasonal dishes made with locally sourced ingredients.\n\nIf the weather is dry but still quite cool, you might want to try some outdoor dining at a café with a heated terrace. Some good options include Café Papeneiland or De Pijp's Café Restaurant. These places offer a cozy atmosphere and a chance to enjoy your meal while still being outside.\n\nFor a cold day treat, consider trying some seasonal specials like hot chocolate or mulled wine. You can find these at many cafes and restaurants throughout the city. Some popular options include The Flying Pan, which serves up delicious waffles with hot chocolate, or De Kas, which offers a variety of winter desserts.",
        "fitness_options": "If you're looking to get some exercise outdoors in Amsterdam today, it's a decent day for jogging or walking as the weather is mostly cloudy but dry. The temperature is around 0°C, which is not too cold, and the winds are relatively light at 4.7 km/h from the north-east. However, if you're planning to engage in more intense outdoor activities like skiing or surfing, it's probably not the best day as there's no snow on the ground and the sea conditions might be rough due to the expected wind gusts.\n\nFor tomorrow, things look a bit better for outdoor enthusiasts. The temperature is expected to rise to around 2°C, making it a good day for cycling or jogging in Amsterdam. If you're planning to hit the slopes, there's still no snow on the ground, but if you're willing to travel a bit further out of the city, you might find some decent skiing conditions.\n\nIf you'd rather stay indoors and get your exercise fix, there are plenty of options available in Amsterdam. For a good workout, you could head to one of the many gyms in the city, such as the Fitness First or the B-Fit gym. If you're looking for something a bit more relaxing, consider visiting one of the yoga studios like Yoga House or Yoga Studio Amsterdam. Alternatively, if you're feeling adventurous and want to try indoor climbing, check out the Amsterdam Climbing Gym.",
        "health_advice": "When it comes to dressing for the weather in Amsterdam today, you should prioritize warmth due to the chilly temperatures ranging from -0.3°C to 1.9°C. Wear layers that can be easily added or removed as needed, such as a base layer, sweater, and coat. Don't forget warm socks and gloves to keep your extremities cozy.\n\nThe wind speed is relatively low at 4.7 km/h, but it's still blowing from the north-east, which might make you feel cooler than the actual temperature. Consider wearing clothing that provides some wind protection, like a scarf or hat. As for precipitation, there's no chance of rain today, so you can skip bringing an umbrella.\n\nFor tomorrow, temperatures will be slightly warmer, with highs around 2.0°C and lows around -0.4°C. You might want to start shedding those extra layers as the day warms up. However, it's still a good idea to bring some light clothing for layering purposes. The wind speed is expected to pick up tomorrow afternoon, so be prepared with some wind-resistant gear.\n\nAir quality in Amsterdam today and tomorrow is not a concern, with no pollution alerts or advisories issued by local authorities. If you have allergies, keep an eye on pollen counts, which are typically low during this time of year. However, if you're sensitive to mold or mildew, be aware that damp weather can exacerbate these conditions.\n\nThe UV index in Amsterdam today is relatively low due to the cloudy skies, but it's still a good idea to apply sunscreen with at least SPF 30 for any exposed skin. Tomorrow, with more sunshine expected, the UV index will likely increase, so don't forget your sun protection. Even on colder days, the sun's rays can be strong, especially in the late morning and early afternoon.",
        "historical_averages": "Here's a summary of the historical weather comparisons and seasonal trends based on the data provided:\n\nAmsterdam is experiencing mostly cloudy conditions today with a mild temperature of -0.3°C, which is relatively cold compared to typical winter days in the city. The wind speed is moderate at 4.7 km/h from the north-east, but it's expected to pick up later in the day. Looking back at previous years, this temperature is slightly below average for this time of year.\n\nIn terms of seasonal trends, Amsterdam typically sees a mix of cold and mild days during winter, with temperatures often fluctuating between -5°C and 10°C. Today's forecasted high of 1.9°C is on the lower end of this range, suggesting that it may be one of the colder days in recent weeks. However, it's worth noting that there's no precipitation expected today or tomorrow, which is consistent with typical winter weather patterns in Amsterdam.\n\nTomorrow's forecast is for a slightly warmer day, with a high temperature of 2.0°C and a low of -0.4°C. This is still relatively cold compared to average temperatures this time of year, but it suggests that the city may be experiencing a brief warm-up before returning to colder conditions. Overall, today's weather is consistent with typical winter patterns in Amsterdam, with cold temperatures and moderate winds.",
        "local_insights": "If you're visiting Amsterdam during winter, consider checking out the ice rinks that pop up in various locations around the city. The weather is mostly cloudy today, but it's not too cold, making it perfect for a fun day on the ice. Temperatures will fluctuate between -0.4°C and 1.9°C, so dress warmly.\n\nFor photography enthusiasts, Amsterdam has plenty of photogenic locations to explore. In winter, the city takes on a serene beauty with its snow-covered canals and buildings. Look for spots with interesting light effects, such as the way the fog rolls in off the water or the soft glow of streetlights reflecting off the snow. Some ideal spots include the Rijksmuseum's gardens, which are particularly beautiful when covered in frost, and the Jordaan neighborhood, where you can capture charming scenes of locals going about their daily lives.\n\nIf you're planning to visit a market during your stay, here are some schedules to keep in mind. The Albert Cuyp Market is open every day except Sundays from 9:00 AM to 5:00 PM, while the Waterlooplein Flea Market takes place on Mondays and Saturdays from 8:30 AM to 3:00 PM. For a more local experience, try visiting one of the many farmers' markets that pop up throughout the city, such as the Noordermarkt or the Lindengracht Market, which usually take place on Fridays from 9:00 AM to 1:00 PM and Saturdays from 9:30 AM to 3:30 PM.",
        "tourism_insights": "If you're planning to stay in Amsterdam, there are still plenty of fun activities to do despite the cloudy weather. You could visit one of the city's many museums, such as the Rijksmuseum or the Van Gogh Museum, and spend a few hours learning about Dutch art and history. Alternatively, take a stroll through the beautiful Vondelpark, which is especially lovely on a crisp winter morning. If you're feeling adventurous, rent a bike and explore the city's canals and bridges.\n\nIf you'd rather get out of the city for a day, consider taking a trip to the nearby snowy mountains. The Netherlands has several ski resorts within driving distance from Amsterdam, such as the SnowWorld in Landgraaf or the Papendal Ski Resort. You could spend the day skiing, snowboarding, or even just building a snowman and having a snowball fight. If you're not up for skiing, there are plenty of other winter activities to enjoy, like ice skating or taking a horse-drawn sleigh ride.\n\nIf you'd rather stay in Amsterdam but still want to get some sunshine, consider visiting one of the city's many indoor gardens or greenhouses. The Amsterdam Botanical Gardens is a beautiful spot to escape the cloudy weather and get some fresh air (even if it's not directly from outside). You could also visit the Tropical Museum, which features a lush tropical garden with plants and flowers from around the world.",
        "travel_tips": "Traffic and Road Conditions: The roads are likely to be clear today as there's no precipitation forecasted in Amsterdam. However, drivers should still exercise caution due to fluctuating temperatures between -0.4°C and 1.9°C, which may cause icy patches on the road, especially during the late afternoon when winds pick up.\n\nPublic Transit Schedules: Buses, trams, and trains are expected to run as normal today with no disruptions anticipated from weather conditions. However, commuters should check schedules in advance for any possible delays due to increased traffic or road conditions.\n\nCycling and Walking Routes: Cyclists can expect dry roads today but may need to be cautious of strong winds blowing at 12.6 km/h in the late afternoon. For walkers, sheltered routes such as those under bridges or in parks might provide some protection from the wind.",
        "utilities_info": "To stay warm during this cold snap, consider turning up your thermostat to at least 18-20°C when you're home, but don't forget to lower it when you leave or go to bed. You can also use thick curtains or blinds to keep warmth in and cold out. If you have a programmable thermostat, set it to adjust the temperature automatically.\n\nFor cooling advice during heatwaves, try keeping your windows open at night to let cool air in, then close them during the day to keep the heat out. Use fans to circulate the air and make your home feel cooler without raising the temperature. You can also use light-colored curtains or blinds to reflect sunlight and keep your home cooler.\n\nIn case of a power outage, stay informed with alerts from your utility company. They may send you notifications via email, text message, or social media when there's an outage in your area. Keep a battery-powered radio on hand to stay updated on the status of the outage and any estimated restoration times. If you have a portable charger, use it to keep your phone charged so you can receive important updates.",
        "weather": "Amsterdam, Netherlands\nCurrent weather is mostly cloudy with a temperature of -0.3°C and winds blowing at 4.7 km/h from the north-east.\nThere's no precipitation expected in Amsterdam today.\n\nLooking ahead to the rest of the day, temperatures will fluctuate between -0.4°C and 1.9°C, with the highest wind speed reaching up to 12.6 km/h in the late afternoon.\nPrecipitation is not forecasted for any part of the day.\n\nFor tomorrow, Amsterdam can expect a high temperature of 2.0°C and a low of -0.4°C, with no precipitation expected throughout the day."
      }
    ]
  },
  "success": true
}
```

## **whois_api**
An API for retrieving details about known individuals. This is the default project generated when running `kdeps
new`. It uses request data to handle inputs. To interact with the API using `curl`, run:

```shell
curl 'http://localhost:3000/api/v1/whois' -X GET -d "Neil Armstrong"
```

And outputs:

```json
{
  "errors": [
    {
      "code": 0,
      "message": ""
    }
  ],
  "response": {
    "data": [
      {
        "address": "Lebanon, Ohio, USA (birthplace)",
        "famous_quotes": [
          "That's one small step for man, one giant leap for mankind."
        ],
        "first_name": "Neil",
        "known_for": [
          "First person to walk on the Moon during the Apollo 11 mission",
          "Pioneering astronaut and naval aviator"
        ],
        "last_name": "Armstrong",
        "parents": {
          "father": "Stephen Koenig Armstrong",
          "mother": "Viola Louise Engel"
        }
      }
    ]
  },
  "success": true
}
```

## **huggingface_imagegen_api**
An API that generates images using a Hugging Face model. Before running the project, create a `.env` file containing
your Hugging Face token (`HF_TOKEN`). It uses request parameters to pass input values. To interact with the API using
`curl`, run:

```shell
curl "http://localhost:3000/api/v1/imagegen?q=A+red+panda+holding+a+balloon"
```

And outputs:

```json
{
  "errors": [
    {
      "code": 0,
      "message": ""
    }
  ],
  "response": {
    "data": [
      {
        "file": "data:image/png;base64,iVBORw0KG...",
      }
    ]
  },
  "success": true
}
```

This image:

![A red panda holding a balloon](/assets/redpanda.png)

---

## How to Run
1. Clone this repository.
2. Package the desired project using the following command:

   ```shell
   kdeps package <folder>
   ```

3. Run the packaged project with:

   ```shell
   kdeps run <agentName-version>.kdeps
   ```
