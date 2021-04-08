$(function() {
  let validateCount = 0;
  function validateCountUp() {
    validateCount++;
  }

  function validateCountDown() {
    validateCount = Math.max(0, validateCount - 1);
  }

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
        $(".register button").addClass('disabled');
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
    $(".register button").addClass('disabled');
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
    $(".register button").addClass('disabled');
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
  }

  $(".register button").addClass('disabled');
});
