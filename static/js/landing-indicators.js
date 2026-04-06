(function () {
  'use strict';

  function formatCurrency(value) {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP',
      maximumFractionDigits: 2,
    }).format(value);
  }

  function formatDate(value) {
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return 'Fecha no disponible';
    }
    return new Intl.DateTimeFormat('es-CL', {
      dateStyle: 'short',
      timeStyle: 'short',
      timeZone: 'America/Santiago',
    }).format(date);
  }

  function weatherLabelFromCode(code) {
    var map = {
      0: 'Despejado',
      1: 'Mayormente despejado',
      2: 'Parcial nublado',
      3: 'Nublado',
      45: 'Neblina',
      48: 'Neblina escarchada',
      51: 'Llovizna ligera',
      53: 'Llovizna moderada',
      55: 'Llovizna intensa',
      61: 'Lluvia ligera',
      63: 'Lluvia moderada',
      65: 'Lluvia intensa',
      71: 'Nieve ligera',
      73: 'Nieve moderada',
      75: 'Nieve intensa',
      80: 'Chubascos ligeros',
      81: 'Chubascos moderados',
      82: 'Chubascos intensos',
      95: 'Tormenta electrica',
      96: 'Tormenta con granizo',
      99: 'Tormenta con granizo fuerte',
    };
    return map[code] || 'Sin dato';
  }

  async function fetchWeather(container) {
    var source = container.getAttribute('data-weather-source') || 'https://api.open-meteo.com/v1/forecast';
    var lat = container.getAttribute('data-weather-lat') || '-32.558';
    var lon = container.getAttribute('data-weather-lon') || '-71.445';
    var place = container.getAttribute('data-weather-label') || 'Zona';
    var placeEl = container.querySelector('[data-indicator-value="weather-place"]');
    var weatherEl = container.querySelector('[data-indicator-value="weather"]');

    if (placeEl) {
      placeEl.textContent = place;
    }
    if (!weatherEl) {
      return;
    }

    var params = new URLSearchParams({
      latitude: lat,
      longitude: lon,
      current: 'temperature_2m,weather_code',
      timezone: 'America/Santiago',
    });

    var response = await fetch(source + '?' + params.toString(), {
      method: 'GET',
      cache: 'no-store',
    });
    if (!response.ok) {
      throw new Error('Weather HTTP ' + response.status);
    }

    var payload = await response.json();
    var current = payload.current || {};
    var temperature = typeof current.temperature_2m === 'number'
      ? Math.round(current.temperature_2m)
      : null;
    var weatherCode = typeof current.weather_code === 'number' ? current.weather_code : null;
    var label = weatherLabelFromCode(weatherCode);

    if (temperature === null) {
      weatherEl.textContent = 'No disponible';
      return;
    }

    weatherEl.textContent = temperature + '°C · ' + label;
  }

  async function fetchIndicators(container) {
    var statusEl = document.getElementById('indicatorStatus');
    var errorEl = document.getElementById('indicatorError');
    var endpoint = container.getAttribute('data-source') || 'https://mindicador.cl/api';

    var controller = new AbortController();
    var timeoutId = setTimeout(function () {
      controller.abort();
    }, 7000);

    try {
      var response = await fetch(endpoint, {
        method: 'GET',
        signal: controller.signal,
        cache: 'no-store',
      });

      if (!response.ok) {
        throw new Error('HTTP ' + response.status);
      }

      var payload = await response.json();
      var indicators = {
        uf: payload.uf,
        dolar: payload.dolar,
        utm: payload.utm,
      };

      var latestDate = null;
      Object.keys(indicators).forEach(function (key) {
        var item = indicators[key];
        var valueEl = container.querySelector('[data-indicator-value="' + key + '"]');
        if (!valueEl || !item) {
          return;
        }

        valueEl.textContent = formatCurrency(item.valor);
        if (!latestDate || new Date(item.fecha) > new Date(latestDate)) {
          latestDate = item.fecha;
        }
      });

      if (statusEl) {
        statusEl.textContent = latestDate
          ? 'Actualizado: ' + formatDate(latestDate)
          : 'Valores oficiales de mindicador.cl';
      }
      if (errorEl) {
        errorEl.classList.add('hidden');
      }
    } catch (error) {
      if (statusEl) {
        statusEl.textContent = 'Sin conexion con indicadores';
      }
      if (errorEl) {
        errorEl.classList.remove('hidden');
      }
      console.error('Error cargando indicadores:', error);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.getElementById('market-indicators');
    if (!container) {
      return;
    }
    fetchIndicators(container);
    fetchWeather(container).catch(function (error) {
      var weatherEl = container.querySelector('[data-indicator-value="weather"]');
      if (weatherEl) {
        weatherEl.textContent = 'No disponible';
      }
      console.error('Error cargando clima:', error);
    });
  });
})();
