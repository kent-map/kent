jQuery( document ).ready(function() {

  // Add active class to accordion header when selected.
  jQuery('.view-program-grid .paragraphs-item-accordion').on('show.bs.collapse', function(e) {
    jQuery(e.target).prev('.panel-heading').addClass('active');
  });
  jQuery('.paragraphs-item-accordion').on('hide.bs.collapse', function(e) {
    jQuery(e.target).prev('.panel-heading').removeClass('active');
  });


  // If you would like to target a specific accordion item when loading a page.
  if (window.location.hash.substr(1) !== '') {
    var accordionItemName = window.location.hash.substr(1);
    var accordionName = accordionItemName.replace("accordion", "collapse");
    jQuery('[name="'+accordionItemName+'"]').removeClass('collapsed');
    jQuery('#'+accordionName+'').addClass('in');
  }

  // If using a mobile device, then the accordions should scroll to the top when clicked.
  var newWindowWidth = jQuery(window).width();
  if(newWindowWidth < 769) {
    jQuery('.panel-title').click(function () {
      var  id_name  =  jQuery(this).attr('id');
      jQuery('html,body').animate({scrollTop: jQuery('#' + id_name).offset().top - 50}, 500);
    });
  }

  jQuery( "div.tab-pane" ).addClass( "fade" );
  jQuery( "div.tab-pane.active" ).addClass( "in" );

  // Add responsive bootstrap classes and wrappers to all tables.
  jQuery( "table" ).addClass( "table" );
  jQuery( "table" ).wrap( "<div class='table-responsive'></div>" );
  jQuery( "table.table-non-responsive" ).unwrap( "<div class='table-responsive'></div>" );
  jQuery( "table.table-responsive" ).unwrap( "<div class='table-responsive'></div>" );

  // Add bootstrap button classes to existing buttons.
  jQuery( ".button25" ).addClass( "btn btn-primary" );
  jQuery( ".button33" ).addClass( "btn btn-primary" );
  jQuery( ".button50" ).addClass( "btn btn-primary" );
  jQuery( ".button100" ).addClass( "btn btn-primary btn-block" );
  jQuery( ".button100" ).removeClass( "button100" );
  jQuery( ".callout-button" ).addClass( "btn btn-primary" );
  jQuery( ".callout-button-50" ).addClass( "btn btn-primary" );
  jQuery( ".callout-button-75" ).addClass( "btn btn-primary" );
  jQuery( ".callout-button-100" ).addClass( "btn btn-primary btn-block" );
  jQuery( ".small-button" ).addClass( "btn btn-info btn-sm" );
  jQuery( ".small-button-100" ).addClass( "btn btn-info btn-block btn-sm" );
  jQuery( ".large-button" ).addClass( "btn btn-primary" );
  jQuery( ".large-button-100" ).addClass( "btn btn-primary btn-block" );
  jQuery( ".large-button-100" ).removeClass( "large-button-100" );

  // For file upload buttons on webforms, alter classes so they don't appear like submit buttons.
  jQuery( ".form-managed-file button" ).removeClass( "btn-primary" );
  jQuery( ".form-managed-file button" ).addClass( "btn-default" );

  // Add responsive bootstrap classes to any images within content.
  jQuery( "#primary-content img" ).addClass( "img-responsive" );
  // But remove it from hero areas.
  //jQuery( ".hero-text img" ).removeClass( "img-responsive" );

  // Add responsive bootstrap classes to any embedded YouTube and Vimeo videos within paragraph content.
  jQuery( ".media-youtube-video" ).addClass( "embed-responsive embed-responsive-16by9" );
  jQuery( ".media-vimeo-video" ).addClass( "embed-responsive embed-responsive-16by9" );

  // Add arrows to accordions (from front page tabs).
  jQuery( '.tabs-accordion-wrap #views-bootstrap-tab-1 > ul > li > a' ).append( '<span class="glyphicon glyphicon-menu-down"></span>' );

  // Removing context class that interferes with page title.
  jQuery( "#block-og-menu-og-single-menu-block" ).removeClass( "contextual-links-region" );

  // Hide document category exposed filter if no terms are associated.
  if( jQuery('#views-exposed-form-document-list-page #edit-category').has('option').length > 0 ) { } else {
    jQuery("#views-exposed-form-document-list-page").css("display", "none");
  }

   // Adding font awesome arrow to .btn-read-more class.
  jQuery(".btn-read-more").append("<span style='white-space:nowrap;'>&#65279;<i class='fas fa-arrow-right'></i></span>");
  jQuery(".btn-read-more-inverse").append("<span style='white-space:nowrap;'>&#65279;<i class='fas fa-arrow-right fa-white'></i></span>");

  // Showing side menu navigation trail.
  jQuery( ".menu-block-2 .active-trail").parent().next("ul").addClass("in");
  jQuery( ".menu-block-2 .active-trail").prev("button").removeClass("collapsed");

  // Moving side nav from side (full width) to bottom (mobile).
  checkSize();
  jQuery(window).resize(checkSize);

  // Collapse certain tabs to accordions on mobile (small and extra small).
  jQuery('.tab-collapse-accordion').tabCollapse({
    tabsClass: 'hidden-sm hidden-xs',
    accordionClass: 'visible-sm visible-xs'
  });

  var nav = jQuery("#unit-nav");
	var navBtn = jQuery("#nav-toggle");
	var closeNav = jQuery("#close-nav");

	navBtn.on('click', checkNav);
	closeNav.on('click', checkNav);

	function checkNav() {
		if (nav.hasClass("open")) {
			nav.removeClass("open");
			navBtn.addClass("collapsed");
		} else {
			nav.addClass("open");
			navBtn.removeClass("collapsed");
		}
	}

  // Removing links from Grad studies vocab listings as a temporary fix.
  jQuery('.og-name-school-of-graduate-studies .field-name-og-vocabulary a').contents().unwrap();

});

function checkSize() {
  // Move side nav to bottom when style changes to mobile breakpoint.
  if (jQuery("#nav-secondary").css("margin-top") == "30px") {jQuery("#nav-secondary").appendTo("#nav-secondary-mobile");}
  // Move side nav back to side.
  else {jQuery("#nav-secondary").appendTo("#nav-secondary-full");}

  // Move paragraph sub nav to bottom when style changes to mobile breakpoint.
  if (jQuery("#paragraph-sub-menu").css("margin-top") == "1px") {jQuery("#paragraph-sub-menu").appendTo("#nav-secondary-mobile");}
  // Move paragraph sub nav back to original position.
  else {jQuery("#paragraph-sub-menu").appendTo("#nav-secondary-full");}

  // resize the header search box (small input on desktop/tablet)
	if(jQuery(window).width()> 767) {
		jQuery("#header-search:not('.og-name-future-undergraduate-students #header-search, .og-name-future-graduate-students #header-search')").addClass("input-group-sm");

	}
}

 jQuery(document).delegate('#edit-reset','click',function(event) {
    event.preventDefault();
    jQuery('form').each(function(){
    jQuery('form select option').removeAttr('selected');
    jQuery('form input[type=text]').attr('value', '');
    this.reset();
    });
   jQuery('.views-submit-button .form-submit').click();
    return false;
  });

jQuery( document ).ajaxComplete(function() {
  // Add responsive bootstrap classes and wrappers to all tables (when using ajax to paginate or filter views tables).
  jQuery( "table" ).addClass( "table" );
  jQuery( "table" ).wrap( "<div class='table-responsive'></div>" );
  jQuery( "table.table-non-responsive" ).unwrap( "<div class='table-responsive'></div>" );
  jQuery( "table.table-responsive" ).unwrap( "<div class='table-responsive'></div>" );

   // Add active class to accordion header when selected.
  jQuery('.view-program-grid .paragraphs-item-accordion').on('show.bs.collapse', function(e) {
    jQuery(e.target).prev('.panel-heading').addClass('active');
  });
  jQuery('.paragraphs-item-accordion').on('hide.bs.collapse', function(e) {
    jQuery(e.target).prev('.panel-heading').removeClass('active');
  });

});


	/* =================================================================
	*  Keep focus on auto-submitted text-fields without surrounding block
	*  ============================================================== */

function SetCaretAtEnd(elem) {
  var elemLen = elem.value.length;
  // For IE Only
  if (document.selection) {
      // Set focus
      elem.focus();
      // Use IE Ranges
      var oSel = document.selection.createRange();
      // Reset position to 0 & then set at end
      oSel.moveStart('character', -elemLen);
      oSel.moveStart('character', elemLen);
      oSel.moveEnd('character', 0);
      oSel.select();
  }
  else if (elem.selectionStart || elem.selectionStart == '0') {
      // Firefox/Chrome
      elem.selectionStart = elemLen;
      elem.selectionEnd = elemLen;
      elem.focus();
  } // if
} // SetCaretAtEnd()

var textboxToFocus = {};

jQuery(function($) {
  var addFocusReminder = function(textbox) {
    textbox.bind('keypress keyup', function(e) {
      textboxToFocus.formid = $(this).closest('form').attr('id');
      textboxToFocus.name = $(this).attr('name');

      if(e.type == 'keypress') {
        if(e.keyCode != 8) { // everything except return
          textboxToFocus.value = $(this).val() + String.fromCharCode(e.charCode);
        } else {
          textboxToFocus.value = $(this).val().substr(0, $(this).val().length-1)
        }
      }
      else { // keyup
        textboxToFocus.value = $(this).val();
      }
    });
  }

  addFocusReminder($('.view-filters input:text.ctools-auto-submit-processed'));
  $(document).ajaxComplete(function(event,request, settings) {
    if(typeof textboxToFocus.formid !== 'undefined') {
	    // Supervisors form
	    var textValue = document.getElementsByName('keyword');
	    if(textValue.length > 0) {
   	    if(textValue[0].value != "") {
          var textBox = $('#' + textboxToFocus.formid + ' input:text[name="' + textboxToFocus.name + '"]');
          textBox.val(textboxToFocus.value);
          SetCaretAtEnd(textBox[0]);
          addFocusReminder(textBox);
        }
      }
      // Undergraduate program form
      var textValue2 = document.getElementsByName('program_search');
      if(textValue2.length > 0) {
	      if(textValue2[0].value != "") {
          var textBox = $('#' + textboxToFocus.formid + ' input:text[name="' + textboxToFocus.name + '"]');
          textBox.val(textboxToFocus.value);
          SetCaretAtEnd(textBox[0]);
          addFocusReminder(textBox);
        }
      }
    }
  });
});

	/* =================================================================
	*  Not my brightest idea, copying from ctools auto-submit.js to over-ride delay amount
	*  ============================================================== */

(function($){

Drupal.behaviors.CToolsAutoSubmit = {
  attach: function(context) {
    // 'this' references the form element
    function triggerSubmit (e) {
      if ($.contains(document.body, this)) {
        var $this = $(this);
        if (!$this.hasClass('ctools-ajaxing')) {
          $this.find('.ctools-auto-submit-click').click();
        }
      }
    }

    // the change event bubbles so we only need to bind it to the outer form
    $('form.ctools-auto-submit-full-form', context)
      .add('.ctools-auto-submit', context)
      .filter('form, select, input:not(:text, :submit)')
      .once('ctools-auto-submit')
      .change(function (e) {
        // don't trigger on text change for full-form
        if ($(e.target).is(':not(:text, :submit, .ctools-auto-submit-exclude)')) {
          triggerSubmit.call(e.target.form);
        }
      });

    // e.keyCode: key
    var discardKeyCode = [
      16, // shift
      17, // ctrl
      18, // alt
      20, // caps lock
      33, // page up
      34, // page down
      35, // end
      36, // home
      37, // left arrow
      38, // up arrow
      39, // right arrow
      40, // down arrow
       9, // tab
      13, // enter
      27  // esc
    ];
    // Don't wait for change event on textfields
    $('.ctools-auto-submit-full-form input:text, input:text.ctools-auto-submit', context)
      .filter(':not(.ctools-auto-submit-exclude)')
      .once('ctools-auto-submit', function () {
        // each textinput element has his own timeout
        var timeoutID = 0;
        $(this)
          .bind('keydown keyup', function (e) {
            if ($.inArray(e.keyCode, discardKeyCode) === -1) {
              timeoutID && clearTimeout(timeoutID);
            }
          })
          .keyup(function(e) {
            if ($.inArray(e.keyCode, discardKeyCode) === -1) {
              timeoutID = setTimeout($.proxy(triggerSubmit, this.form), 250);
            }
          })
          .bind('change', function (e) {
            if ($.inArray(e.keyCode, discardKeyCode) === -1) {
              timeoutID = setTimeout($.proxy(triggerSubmit, this.form), 250);
            }
          });
      });
  }
}
})(jQuery);

