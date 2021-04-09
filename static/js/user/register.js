$(function() {
  function existsUser(userName) {
    return $.ajax({
      url: `/user/${userName}/exists`,
      contentType: 'application/json;charset=UTF-8',
      type: 'GET'
    });
  }

  class ValidationError extends Error {
    constructor(message) {
      super(message);
      this.name = "ValidationError";
    }
  }


  $("#login-name").blur(function() {
    var loginName = $(this);
    try {
      checkSpace(loginName.val());
      checkLength(loginName.val(), 4);
      checkAlphabetAndNumber(loginName.val());
      checkSpecificSymbols(loginName.val());
      errMsg = null;
      existsUser(loginName.val()).done(function(data) {
        if($.parseJSON(data).status) {
          errMsg = 'すでに存在するIDです。';
          invalid(loginName, errMsg);
        }
      }).fail(function(data) {
        errMsg = 'ログインIDの取得に失敗しました。';
        invalid(loginName, errMsg);
      }).always(function(data) {
        if (!errMsg) { valid(loginName); }
      });
    } catch (e) {
      invalid(loginName, e.message);
    }
  });

  $("#password").blur(function() {
    var password = $(this);
    var confirmPassword = $("#confirm-password");
    try {
      checkLength(password.val(), 6);
    } catch (e) {
      invalid(password, e.message);
      return;
    }

    try {
      checkPassword(password.val(), confirmPassword.val());
      valid(password);
      valid(confirmPassword);
    } catch (e) {
      if (confirmPassword.val().length > 0) {
        invalid(password, e.message);
        invalid(confirmPassword, e.message);
      }
    }
  });

  $("#confirm-password").blur(function() {
    var confirmPassword = $(this);
    var password = $("#password");
    if (password.val().length == 0) {
      return;
    }
    try {
      checkLength(password.val(), 6);
      checkPassword(password.val(), confirmPassword.val());
      valid(password);
      valid(confirmPassword);
    } catch(e) {
      invalid(password, e.message);
      invalid(confirmPassword, e.message);
    }
  });

  $("#name").blur(function() {
    var name = $(this);
    try {
      checkLength(name.val(), 1);
      checkSpecificSymbols(name.val());
      valid(name);
    } catch (e) {
      invalid(name, e.message);
    }
  });

  $("input:radio[name=gender]").change(function() {
    $(this).parent().parent().find('label.invalid').text('');
    $(this).parent().parent().find('i.bi').addClass('is-valid');
    $(this).parent().parent().find('i.bi').removeClass('d-none');
  });

  $("#birth-year").blur(function() {
    validateBirth();
  });

  $("#birth-month").blur(function() {
    validateBirth();
  });
  
  $("#birth-day").blur(function() {
    validateBirth();
  });

  function validateBirth() {
    var year = $("#birth-year");
    var month = $("#birth-month");
    var day = $("#birth-day");
    try {
      if (year.val().length == 0 || month.val().length == 0 || day.val().length == 0) {
        disabledButton();
      }

      if (year.val().length > 0){
        if (!isValidDigit(year.val(), 4)) {
          throw new ValidationError('西暦は4桁誤入力ください。');
        }
        if (!isBetweenValue(year.val(), 1900, new Date().getFullYear())) {
          throw new ValidationError('西暦の値が不正です。');
        }
      }

      if (month.val().length > 0 && !isValidMonth(month.val())) {
        throw new ValidationError('月の値が不正です。');
      }

      if (day.val().length > 0 && !isValidDay(day.val())) {
        throw new ValidationError('日の値が不正です。');
      }

      validForBirth(year);
      if (year.val().length > 0 && month.val().length > 0 && day.val().length > 0) {
        validForBirth(year, true);
      }
    } catch (e) {
      invalidForBirth(year, e.message);
    }
  }

  function isValidDigit(str, digit) {
    return str.length == digit;
  }

  function isValidMonth(val) {
    return isBetweenValue(val, 1, 12);
  }

  function isValidDay(val) {
    return isBetweenValue(val, 1, 31);
  }

  function isBetweenValue(target, min, max) {
    return min <= target && target <= max;
  }

  function checkSpecificSymbols(str) {
    var reg = new RegExp(/[!"#$%&'()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]/g);
    if(reg.test(str)) {
      throw new ValidationError(`特殊記号（!"#$%&'()*+-.,:;<=>?@[]\^-{}|~）は利用できません。`);
    }
  }

  function checkPassword(password, confirmPassword) {
    if (password != confirmPassword) {
      throw new ValidationError('パスワードが異なります。');
    }
  }

  function checkSpace(str) {
    if (str.match(/\s/g)) {
      throw new ValidationError('空白は使わないでください。');
    }
  }

  function checkLength(str, length) {
    if (str.length < length) {
      throw new ValidationError(`${length}文字以上入力してください。`);
    }
  }

  function checkAlphabetAndNumber(str) {
    if (str.match(/[^A-Za-z0-9]+/)) {
      throw new ValidationError('英数字のみ入力してください。');
    }
  }

  function invalidForBirth(inputEle, text) {
    inputEle.parent().parent().parent().find('label.invalid').text(text);
    inputEle.parent().parent().parent().find('i.bi').addClass('d-none');
    disabledButton();
  }

  function validForBirth(inputEle, isAllGreen = false) {
    inputEle.parent().parent().parent().find('label.invalid').text('');
    if (isAllGreen) {
      inputEle.parent().parent().parent().find('i.bi').removeClass('d-none');
      inputEle.parent().parent().parent().find('i.bi').addClass('is-valid');
      tryEnableUpdateButton();
    } else {
      inputEle.parent().parent().parent().find('i.bi').addClass('d-none');
      inputEle.parent().parent().parent().find('i.bi').removeClass('is-valid');
    }
  }

  function invalid(inputEle, text) {
    inputEle.parent().find('label.invalid').text(text);
    inputEle.removeClass('is-valid');
    inputEle.addClass('is-invalid');
    disabledButton();
  }

  function valid(inputEle) {
    inputEle.parent().find('label.invalid').text('');
    inputEle.removeClass('is-invalid');
    inputEle.addClass('is-valid');
    tryEnableUpdateButton();
  }

  function tryEnableUpdateButton() {
    if ($('#register .is-valid').length == 6) {
      $(".register button").removeClass('disabled');
    }
    if ($('#user-modify-password .is-valid').length == 2) {
      $(".modify button").removeClass('disabled');
    }
    if ($('#user-modify .is-valid').length == 3) {
      $(".modify button").removeClass('disabled');
    }
  }

  function disabledButton() {
    $(".register button").addClass('disabled');
    $(".modify button").addClass('disabled');
  }

  $(".register button").addClass('disabled');

  $("#first-name").blur(function() {
    validateFullName();
  });

  $("#last-name").blur(function() {
    validateFullName();
  });

  function validateFullName() {
    var firstName = $('#first-name');
    var lastName = $('#last-name');
    try {
      if (firstName.val().length > 0 && lastName.val().length > 0) {
        checkSpace(firstName.val());
        checkSpace(lastName.val());
        checkSpecificSymbols(firstName.val());
        checkSpecificSymbols(lastName.val());
        firstName.parent().parent().parent().find('label.invalid').text("");
        firstName.parent().parent().parent().find('i.bi').removeClass('d-none');
        tryEnableUpdateButton();
      } else if (firstName.val().length > 0 && lastName.val().length == 0 ||
        firstName.val().length == 0 && lastName.val().length > 0) {
        throw new ValidationError('本名はいずれの項目も入力してください。');
      } else if (firstName.val().length == 0 && lastName.val().length == 0) {
        firstName.parent().parent().parent().find('label.invalid').text("");
        firstName.parent().parent().parent().find('i.bi').addClass('d-none');
        tryEnableUpdateButton();
      }
    } catch (e) {
      firstName.parent().parent().parent().find('label.invalid').text(e.message);
      firstName.parent().parent().parent().find('i.bi').addClass('d-none');
      disabledButton();
      return false;
    }
    return true;
  }

  $('#user-modify form').submit(function(){
    return validateFullName();
  })
});
