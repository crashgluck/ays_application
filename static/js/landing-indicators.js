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
  });
})();
