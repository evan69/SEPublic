﻿// === COMPRESSED FOR SECURITY QUESTIONS === //
/*! jquery.avgrund - v1.3.2 (http://labs.voronianski.com/jquery.avgrund.js) */
(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory)
    } else if (typeof exports === 'object') {
        module.exports = factory
    } else {
        factory(jQuery)
    }
} (function($) {
    $.fn.avgrund = function(options) {
        var defaults = {
            width: 380,
            height: 280,
            showClose: false,
            showCloseText: '',
            closeByEscape: true,
            closeByDocument: true,
            holderClass: '',
            overlayClass: '',
            enableStackAnimation: false,
            onBlurContainer: '#box_left, #box_right',
            openOnEvent: true,
            setEvent: 'click',
            onLoad: false,
            onUnload: false,
            template: ''
        };
        options = $.extend(defaults, options);
        return this.each(function() {
            var self = $(this),
            body = $('body'),
            maxWidth = options.width > 640 ? 640 : options.width,
            maxHeight = options.height > 350 ? 350 : options.height,
            template = typeof options.template === 'function' ? options.template(self) : options.template;
            body.addClass('avgrund-ready');
            if ($('.avgrund-overlay').length === 0) {
                body.append('<div class="avgrund-overlay ' + options.overlayClass + '"></div>')
            }
            if (options.onBlurContainer !== '') {
                $(options.onBlurContainer).addClass('avgrund-blur')
            }
            function onDocumentKeyup(e) {
                if (options.closeByEscape) {
                    if (e.keyCode === 27) {
                        deactivate()
                    }
                }
            }
            function onDocumentClick(e) {
                if (options.closeByDocument) {
                    if ($(e.target).is('.avgrund-overlay, .avgrund-close')) {
                        e.preventDefault();
                        deactivate()
                    }
                } else if ($(e.target).is('.avgrund-close')) {
                    e.preventDefault();
                    deactivate()
                }
            }
            function activate() {
                if (typeof options.onLoad === 'function') {
                    options.onLoad(self)
                }
                setTimeout(function() {
                    body.addClass('avgrund-active')
                },
                100);
                var $popin = $('<div class="avgrund-popin ' + options.holderClass + '"></div>');
                $popin.append(template);
                body.append($popin);
                $('.avgrund-popin').css({
                    'width': maxWidth + 'px',
                    'height': maxHeight + 'px',
                    'margin-left': '-' + (maxWidth / 2 + 10) + 'px',
                    'margin-top': '-' + (maxHeight / 2 + 10) + 'px'
                });
                if (options.showClose) {
                    $('.avgrund-popin').append('<a href="#" class="avgrund-close">' + options.showCloseText + '</a>')
                }
                if (options.enableStackAnimation) {
                    $('.avgrund-popin').addClass('stack')
                }
                body.bind('keyup', onDocumentKeyup).bind('click', onDocumentClick)
            }
            function deactivate() {
                body.unbind('keyup', onDocumentKeyup).unbind('click', onDocumentClick).removeClass('avgrund-active');
                setTimeout(function() {
                    $('.avgrund-popin').remove()
                },
                500);
                if (typeof options.onUnload === 'function') {
                    options.onUnload(self)
                }
            }
            if (options.openOnEvent) {
                self.bind(options.setEvent,
                function(e) {
                    e.stopPropagation();
                    if ($(e.target).is('a')) {
                        e.preventDefault()
                    }
                    activate()
                })
            } else {
                activate()
            }
        })
    }
}));