# Examples

This repository features a growing collection of example projects built with Kdeps, including:

## 1. **weather_forecast_api**
A Weather Forecast API that connects to an external provider (https://open-meteo.com) to fetch weather data. It uses
request parameters to pass input values. To interact with the API using `curl`, run:

```shell
curl "http://localhost:3000/api/v1/forecaster?q=What+is+the+weather+in+Amsterdam?"
```

## 2. **whois_api**
An API for retrieving details about known individuals. This is the default project generated when running `kdeps
new`. It uses request data to handle inputs. To interact with the API using `curl`, run:

```shell
curl 'http://localhost:3000/api/v1/whois' -X GET -d "Neil Armstrong"
```

## 3. **huggingface_imagegen_api**
An API that generates images using a Hugging Face model. Before running the project, create a `.env` file containing
your Hugging Face token (`HF_TOKEN`). It uses request parameters to pass input values. To interact with the API using
`curl`, run:

```shell
curl "http://localhost:3000/api/v1/imagegen?q=A+red+panda+holding+a+balloon"
```

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
