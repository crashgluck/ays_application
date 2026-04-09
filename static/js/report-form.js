(function () {
  'use strict';

  function normalizeText(value) {
    return (value || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toUpperCase()
      .trim();
  }

  function isVisible(el) {
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  }

  function fieldValue(elements) {
    if (!elements || elements.length === 0) {
      return '';
    }
    var first = elements[0];
    if (first.type === 'radio') {
      var checked = elements.find(function (item) {
        return item.checked;
      });
      return checked ? checked.value.trim() : '';
    }
    if (first.type === 'checkbox') {
      return elements
        .filter(function (item) {
          return item.checked;
        })
        .map(function (item) {
          return item.value.trim();
        })
        .join('|');
    }
    return (first.value || '').trim();
  }

  function markInvalidInlineFeedback(form) {
    form.querySelectorAll('.is-invalid').forEach(function (field) {
      if (field.parentElement && field.parentElement.querySelector('.field-error-inline')) {
        return;
      }
      var feedback = document.createElement('div');
      feedback.className = 'field-error-inline';
      feedback.textContent = 'Revisa este campo.';
      if (field.parentElement) {
        field.parentElement.appendChild(feedback);
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('.report-form-page form');
    var table = document.getElementById('example');
    var prevButton = document.getElementById('wizardPrev');
    var nextButton = document.getElementById('wizardNext');
    var clearAllButton = document.getElementById('limpiarFormulario');
    var clearStepButton = document.getElementById('limpiarEtapa');
    var stepLabel = document.getElementById('wizardStepLabel');
    var stepText = document.getElementById('wizardProgressText');
    var changeCounter = document.getElementById('wizardChangeCounter');
    var progressBar = document.getElementById('wizardProgressBar');
    var chipsContainer = document.getElementById('wizardStepChips');
    var subchipsContainer = document.getElementById('wizardSubChips');
    var submitButton = form ? form.querySelector('button[type="submit"]') : null;

    if (!form || !table || !prevButton || !nextButton || !chipsContainer || !submitButton) {
      return;
    }

    markInvalidInlineFeedback(form);

    var stepConfig = [
      { label: 'Clima y Riesgos', markers: ['FECHA'] },
      {
        label: 'RRHH',
        markers: [
          'TURNO ALERTA',
          'RRHH (TABLA NUEVA)',
          'PERSONAL DE TURNO COMUNIDAD',
          'PERSONAL DE TURNO AYS',
          'CARGO',
          'MEDIO/LUGAR',
        ],
      },
      { label: 'Vehiculos', markers: ['VEHICULOS COMUNIDAD'] },
      { label: 'Indicadores', markers: ['INDICADORES'] },
      { label: 'Operativos', markers: ['OPERATIVOS'] },
      { label: 'Presiones', markers: ['PRESIONES'] },
      { label: 'Balizas y Sistema CCTV', markers: ['BALIZAS Y SISTEMA CCTV', 'BALIZAS', 'OTRAS NOVEDADES'] },
    ];

    var rows = Array.from(table.querySelectorAll('tr'));
    var currentStep = 0;
    rows.forEach(function (row) {
      var text = normalizeText(row.textContent);
      var matched = stepConfig.findIndex(function (step) {
        return step.markers.some(function (marker) {
          return text.indexOf(marker) !== -1;
        });
      });
      if (matched >= 0) {
        currentStep = matched;
      }
      row.dataset.wizardStep = String(currentStep);
    });

    // Hard mapping by field-name prefix so RRHH never depends only on text markers.
    rows.forEach(function (row) {
      var rrhhField = row.querySelector(
        'input[name^="rrhh_"], select[name^="rrhh_"], textarea[name^="rrhh_"]'
      );
      if (rrhhField) {
        row.dataset.wizardStep = '1';
      }
    });

    function stepHasFields(stepIndex) {
      return rows.some(function (row) {
        return Number(row.dataset.wizardStep) === stepIndex && !!row.querySelector('input, select, textarea');
      });
    }

    function stepHasRows(stepIndex) {
      return rows.some(function (row) {
        return Number(row.dataset.wizardStep) === stepIndex;
      });
    }

    // Safety net for deployments with partial template/static cache mismatch:
    // if RRHH step has no fields, force-map RRHH-like rows to step 2.
    if (!stepHasFields(1)) {
      rows.forEach(function (row) {
        var text = normalizeText(row.textContent);
        var isRrhhRow =
          row.classList.contains('rrhh-data-row') ||
          text.indexOf('TURNO ALERTA') !== -1 ||
          text.indexOf('PERSONAL DE TURNO COMUNIDAD') !== -1 ||
          text.indexOf('PERSONAL DE TURNO AYS') !== -1 ||
          (text.indexOf('CARGO') !== -1 && text.indexOf('MEDIO/LUGAR') !== -1) ||
          (text.indexOf('CARGO') !== -1 && text.indexOf('MEDIO') !== -1);
        if (isRrhhRow) {
          row.dataset.wizardStep = '1';
        }
      });
    }

    var totalSteps = stepConfig.length;
    var stage = 0;
    var chips = [];

    var namedElements = {};
    var initialValues = {};
    var requiredByName = {};

    Array.from(form.querySelectorAll('input, select, textarea')).forEach(function (field) {
      if (!field.name || field.name === 'csrfmiddlewaretoken' || field.type === 'hidden') {
        return;
      }
      if (!namedElements[field.name]) {
        namedElements[field.name] = [];
      }
      namedElements[field.name].push(field);
      requiredByName[field.name] = requiredByName[field.name] || !!field.required;
    });

    Object.keys(namedElements).forEach(function (name) {
      initialValues[name] = fieldValue(namedElements[name]);
    });

    function rowFieldNames(row, requiredOnly) {
      var names = [];
      row.querySelectorAll('input, select, textarea').forEach(function (field) {
        if (!field.name || field.name === 'csrfmiddlewaretoken' || field.type === 'hidden') {
          return;
        }
        if (requiredOnly && !requiredByName[field.name]) {
          return;
        }
        if (names.indexOf(field.name) === -1) {
          names.push(field.name);
        }
      });
      return names;
    }

    function stageFieldNames(stepIndex, requiredOnly) {
      var names = [];
      rows.forEach(function (row) {
        if (Number(row.dataset.wizardStep) !== stepIndex) {
          return;
        }
        rowFieldNames(row, requiredOnly).forEach(function (name) {
          if (names.indexOf(name) === -1) {
            names.push(name);
          }
        });
      });
      return names;
    }

    function stageStats(stepIndex) {
      var names = stageFieldNames(stepIndex, true);
      if (names.length === 0) {
        names = stageFieldNames(stepIndex, false).filter(function (name) {
          return initialValues[name] !== '' || fieldValue(namedElements[name]) !== '';
        });
      }
      if (names.length === 0) {
        names = stageFieldNames(stepIndex, false);
      }
      var filled = 0;
      var changed = 0;
      var errors = 0;

      names.forEach(function (name) {
        var elements = namedElements[name];
        var value = fieldValue(elements);
        if (value !== '') {
          filled += 1;
        }
        if (value !== initialValues[name]) {
          changed += 1;
        }
        var hasError = elements.some(function (el) {
          return el.classList.contains('is-invalid');
        });
        if (hasError) {
          errors += 1;
        }
      });

      return {
        total: names.length,
        filled: filled,
        changed: changed,
        errors: errors,
        pending: Math.max(names.length - filled, 0),
      };
    }

    function totalChangedCount() {
      return Object.keys(namedElements).reduce(function (acc, name) {
        return acc + (fieldValue(namedElements[name]) !== initialValues[name] ? 1 : 0);
      }, 0);
    }

    function updateFieldVisualState(name) {
      var elements = namedElements[name];
      if (!elements || elements.length === 0) {
        return;
      }
      var current = fieldValue(elements);
      var initial = initialValues[name];
      var isPrefilled = initial !== '';
      var isChanged = current !== initial;

      elements.forEach(function (el) {
        el.classList.toggle('field-prefilled', isPrefilled);
        el.classList.toggle('field-changed', isChanged);
        var cell = el.closest('td');
        if (cell) {
          cell.classList.toggle('cell-prefilled', isPrefilled);
          cell.classList.toggle('cell-changed', isChanged);
        }
      });
    }

    function updateRRHHRowStates() {
      table.querySelectorAll('.rrhh-data-row').forEach(function (row) {
        var fields = row.querySelectorAll('input, select, textarea');
        if (!fields.length) {
          return;
        }
        var filled = Array.from(fields).some(function (field) {
          if (field.type === 'radio') {
            var group = namedElements[field.name] || [];
            return fieldValue(group) !== '';
          }
          return (field.value || '').trim() !== '';
        });
        row.classList.toggle('rrhh-row-complete', filled);
      });
    }

    function ensureChips() {
      chipsContainer.innerHTML = '';
      chips = [];
      for (var i = 0; i < totalSteps; i++) {
        var chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'report-wizard-chip';
        chip.dataset.stepIndex = String(i);
        chip.innerHTML = '<span class="chip-label"></span>';
        chip.addEventListener('click', function (event) {
          showStep(Number(event.currentTarget.dataset.stepIndex));
        });
        chipsContainer.appendChild(chip);
        chips.push(chip);
      }
    }

    function refreshChips() {
      chips.forEach(function (chip, index) {
        var stats = stageStats(index);
        var label = (index + 1) + '. ' + stepConfig[index].label;
        chip.querySelector('.chip-label').textContent = label;
        chip.classList.toggle('active', index === stage);
      });

      if (changeCounter) {
        changeCounter.textContent = 'Cambios detectados: ' + totalChangedCount();
      }
    }

    function focusFirstField(stepIndex) {
      var targetRow = rows.find(function (row) {
        if (Number(row.dataset.wizardStep) !== stepIndex) {
          return false;
        }
        return !!row.querySelector('input, select, textarea');
      });
      if (!targetRow) {
        return;
      }
      var targetField = targetRow.querySelector('input:not([type="hidden"]), select, textarea');
      if (targetField && isVisible(targetField)) {
        targetField.focus({ preventScroll: true });
      }
    }

    function rowByMarker(stepIndex, markerText) {
      return rows.find(function (row) {
        if (Number(row.dataset.wizardStep) !== stepIndex) {
          return false;
        }
        return normalizeText(row.textContent).indexOf(normalizeText(markerText)) !== -1;
      });
    }

    function renderSubChips(stepIndex) {
      if (!subchipsContainer) {
        return;
      }
      var configs = {
        1: [
          { label: 'Turno Alerta', marker: 'TURNO ALERTA' },
          { label: 'Turno Comunidad', marker: 'PERSONAL DE TURNO COMUNIDAD' },
          { label: 'Turno AyS', marker: 'PERSONAL DE TURNO AYS' },
        ],
        3: [
          { label: 'Electricos', marker: 'ELEC' },
          { label: 'Solar', marker: 'SOLAR' },
          { label: 'Inversores', marker: 'INVERSORES' },
          { label: 'Atlas/GPS', marker: 'SISTEMA ATLAS/GPS' },
          { label: 'Portones', marker: 'PORTONES' },
        ],
        6: [
          { label: 'Balizas', marker: 'BALIZAS' },
          { label: 'Otras novedades', marker: 'OTRAS NOVEDADES' },
        ],
      };

      var group = configs[stepIndex];
      if (!group) {
        subchipsContainer.hidden = true;
        subchipsContainer.innerHTML = '';
        return;
      }

      subchipsContainer.hidden = false;
      subchipsContainer.innerHTML = '';
      group.forEach(function (entry) {
        var row = rowByMarker(stepIndex, entry.marker);
        if (!row) {
          return;
        }
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'report-subchip';
        button.textContent = entry.label;
        button.addEventListener('click', function () {
          row.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        subchipsContainer.appendChild(button);
      });
      if (!subchipsContainer.children.length) {
        subchipsContainer.hidden = true;
      }
    }

    function showStep(stepIndex) {
      stage = Math.max(0, Math.min(stepIndex, totalSteps - 1));

      // Final fallback: if selected stage has no rows, move to first non-empty stage.
      if (!stepHasRows(stage)) {
        var fallbackStage = 0;
        while (fallbackStage < totalSteps && !stepHasRows(fallbackStage)) {
          fallbackStage += 1;
        }
        if (fallbackStage < totalSteps) {
          stage = fallbackStage;
        }
      }

      rows.forEach(function (row) {
        row.hidden = Number(row.dataset.wizardStep) !== stage;
      });

      var stats = stageStats(stage);
      stepLabel.textContent = 'Etapa ' + (stage + 1) + ': ' + stepConfig[stage].label;
      stepText.textContent = (stage + 1) + '/' + totalSteps;
      progressBar.style.width = (((stage + 1) / totalSteps) * 100).toFixed(2) + '%';
      prevButton.disabled = stage === 0;
      nextButton.textContent = stage === totalSteps - 1 ? 'Ir a guardar' : 'Siguiente';
      refreshChips();
      renderSubChips(stage);
      focusFirstField(stage);
      table.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function clearNamedFields(fieldNames) {
      fieldNames.forEach(function (name) {
        var elements = namedElements[name] || [];
        if (!elements.length) {
          return;
        }
        var first = elements[0];
        if (first.type === 'radio' || first.type === 'checkbox') {
          elements.forEach(function (field) {
            field.checked = false;
          });
        } else if (first.tagName === 'SELECT') {
          first.selectedIndex = 0;
        } else {
          first.value = '';
        }
        updateFieldVisualState(name);
      });
      updateRRHHRowStates();
      refreshChips();
    }

    function clearCurrentStep() {
      var names = stageFieldNames(stage, false);
      if (!names.length) {
        return;
      }
      var approved = window.confirm(
        'Se limpiaran solo los campos de esta etapa. ¿Deseas continuar?'
      );
      if (!approved) {
        return;
      }
      clearNamedFields(names);
      showStep(stage);
    }

    function clearAllSteps() {
      var approved = window.confirm(
        'Se reiniciaran TODOS los campos del formulario. Esta accion no se puede deshacer.'
      );
      if (!approved) {
        return;
      }
      clearNamedFields(Object.keys(namedElements));
      showStep(0);
    }

    function focusNextField(currentField) {
      var focusables = Array.from(
        form.querySelectorAll('input, select, textarea, button')
      ).filter(function (field) {
        if (field.disabled || field.type === 'hidden' || !isVisible(field)) {
          return false;
        }
        return field.name !== 'csrfmiddlewaretoken';
      });
      var index = focusables.indexOf(currentField);
      if (index === -1 || index >= focusables.length - 1) {
        return;
      }
      focusables[index + 1].focus();
    }

    ensureChips();

    Object.keys(namedElements).forEach(function (name) {
      updateFieldVisualState(name);
      namedElements[name].forEach(function (field) {
        field.addEventListener('input', function () {
          updateFieldVisualState(name);
          updateRRHHRowStates();
          refreshChips();
        });
        field.addEventListener('change', function () {
          updateFieldVisualState(name);
          updateRRHHRowStates();
          refreshChips();
        });
      });
    });

    updateRRHHRowStates();
    refreshChips();

    prevButton.addEventListener('click', function () {
      showStep(stage - 1);
    });

    nextButton.addEventListener('click', function () {
      if (stage === totalSteps - 1) {
        submitButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
        submitButton.focus();
        return;
      }
      showStep(stage + 1);
    });

    if (clearAllButton) {
      clearAllButton.addEventListener('click', clearAllSteps);
    }
    if (clearStepButton) {
      clearStepButton.addEventListener('click', clearCurrentStep);
    }

    form.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' && event.target && event.target.tagName !== 'TEXTAREA') {
        if (event.target.type === 'submit' || event.target.type === 'button') {
          return;
        }
        event.preventDefault();
        focusNextField(event.target);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (!event.altKey) {
        return;
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        showStep(stage + 1);
      } else if (event.key === 'ArrowLeft') {
        event.preventDefault();
        showStep(stage - 1);
      }
    });

    var firstInvalidField = form.querySelector('.is-invalid');
    if (firstInvalidField) {
      var invalidRow = firstInvalidField.closest('tr');
      if (invalidRow && invalidRow.dataset.wizardStep) {
        showStep(Number(invalidRow.dataset.wizardStep));
        return;
      }
    }

    showStep(0);
  });
})();
