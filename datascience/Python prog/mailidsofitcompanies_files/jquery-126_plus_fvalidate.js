function fValConfig()
{
    /*	Globals.  Modify these to suit your setup
    ------------------------------------------- */
        
    //	Attribute used for fValidate Validator codes
    this.code = 'validators';
    
    //	Attribute used for custom error messages (override built-in error messages)
    this.emsg = 'emsg';
    
    //	Attribute used for pattern with custom validator type
    this.pattern = 'pattern';
    
    //	Change this to the classname you want for the error highlighting
    this.errorClass = 'errHilite';

    //	If you wish fValidate to use only single classNames for errors
    this.useSingleClassNames = false; // or true
    
    //	This is the even that triggers the clearing of the errorClass hilighting
    this.clearEvent = 'change'; // 'change' | 'blur' | null
    
    //	For browsers that don't support attachEvent or addEventListere - override existing events for error reverting?
    this.eventOverride = false;
    
    //	If the bConfirm flag is set to true, the users will be prompted with CONFIRM box with this message
    //	See your language file for this value
    this.confirmMsg = fvalidate.i18n.config.confirmMsg;
    
    //	If user cancels CONFIRM, then this message will be alerted.  If you don't want this alert to show, then
    //	empty the variable (  this.confirmAbortMsg = '';  )
    //	See your langauge file for this value
    this.confirmAbortMsg = fvalidate.i18n.config.confirmAbortMsg;
    
    //	Enter the name/id of your form's submit button here.  Can be a string or array of strings
    this.submitButton = ['Submit','Submit2'];
    
    //	Enter the name/id of your form's reset button here
    this.resetButton = 'Reset';
    
    //	Ender the name or id of the SELECT object here. Make sure you pay attention to the values (CC Types)
    //	used in the case statement for the function validateCC()
    this.ccType = 'Credit_Card_Type';
    
    //	NOTE: The config value below exists for backwards compatibility with fValidate 3.55b.  If you have a newer 
    //	version, use the above this.ccType instead.
    //	Enter the DOM name of the SELECT object here. Make sure you pay attention to the values (CC Types)
    //	used in the case statement for the function validateCC()
    this.ccTypeObj = 'form1.Credit_Card_Type';
    
    //	Element where box errors will appear
    this.boxError = 'errors';
    
    //	Prefix given to all error paragraphs in box error mode
    this.boxErrorPrefix = 'fv_error_';
    
    this.displayName= 'displayName';
}





/***************************************************************************************************
*
*-- Form validation script by Peter Bailey, Copyright (c) 2001-2003
*	Version 5.01b
*	Updated on Feb 07, 2004
*	www.peterbailey.net
*	me@peterbailey.net
*
*	IF YOU USE THIS SCRIPT, GIVE ME CREDIT PLEASE =)
*
*	Visit http://www.peterbailey.net/fValidate/ for more info
*
*	Feel free to contact me with any questions, comments, problems, or suggestions
*
*	Note: This document most easily read with tab spacing set to 4
*
*******************************************************************************************************/

/*	Create static fvalidate object
------------------------------------------- */
if ( typeof fvalidate == 'undefined' )
{
var fvalidate = new Object();
}

/*	Generic event handling
------------------------------------------- */
fvalidate.addEvent = function( obj, evt, fn, useCapture )
{
if ( typeof obj.attachEvent != 'undefined' )
{
    obj.attachEvent( "on" + evt, fn );
}
else if ( typeof obj.attachEventListener != 'undefined' )
{
    obj.addEventListener( evt, fn, Boolean( useCapture ) );
}
}
fvalidate.addEvents = function( obj, evts, fn, useCapture )
{
var i = 0, evt;
while( evt = evts[i++] )
{
    this.addEvent( obj, evt, fn, Boolean( useCapture ) );
}
}

/*	Main validation routine
------------------------------------------- */
function validateForm( f, bConfirm, bDisable, bDisableR, groupError, errorMode )
{
//	Set defaults
bConfirm	= Boolean( bConfirm );
bDisable	= Boolean( bDisable );
bDisableR	= Boolean( bDisableR );
groupError	= Boolean( groupError );
errorMode	= ( typeof errorMode != 'undefined' ) ? parseInt( errorMode, 10 ) : 0;

//	Init vars and fValidate object
var params, fvCode, type;
if ( typeof f.fv == 'undefined' )
{
    f.fv = new fValidate( f, errorMode, groupError );
} else {		
    f.fv._reset();
    f.fv.errorMode = errorMode;
}

//	Loop through all form elements	
var elem, i = 0, attr = f.fv.config.code;
while ( elem = f.elements[i++] )
{
    //	Skip fieldsets
    if ( elem.nodeName == "FIELDSET" ) continue;

    //	Does element have validator attribute? (short-circuit check)
    fvCode			= ( elem[attr] ) ? elem[attr] : elem.getAttribute( attr );
    if ( !( typeof fvCode == 'undefined' || fvCode == null || fvCode == "" ) )
    {
        //	Set params, validation type, and validation state

        params			= fvCode.split( "|" );
        type			= params[0];
        elem.validated	= true;
        
        //	Valid validator type?
        if ( typeof f.fv[type] == 'undefined' )
        {				
            f.fv.devError( [type, elem.name], 'notFound' );
            return false;
        }
        
        //	Check for modifiers
        switch( params.last() )
        {				
            case 'bok'	:	//	bok requested
                params = params.reduce( 1, 1 );
                elem.bok = true;
                break;
            case 'if'	:	//	Conditional validation requested
                params = params.reduce( 1, 1 );
                elem._if_ = true;
                break;
            case 'then'	:	//	Conditional validation requested
                params = params.reduce( 1, 1 );
                elem._then_ = true;
                break;
            default		:	//	No modifiers
                params = params.reduce( 1, 0 );
            
        }

        //	Is element an array?
        if ( /radio|checkbox/.test( elem.type ) )
        {
            //	Set group property
            elem.group = f.elements[elem.name];
        }
        
        //	Add events if not already added
        if ( typeof elem.fName == 'undefined' )
        {
            //	If element is an array			
            if ( typeof elem.group != 'undefined' )
            {
                for ( var j = 0; j < elem.group.length; j++ )				
                {
                    //	Apply event-function to each child
                    if ( f.fv.config.clearEvent != null )
                    {
                    //	fvalidate.addEvent( elem.group.item( j ), fv.config.clearEvent, fv.revertError, false );
                        addEvent( elem.group.item( j ), f.fv.config.clearEvent, f.fv, 'revertError', false );
                    }
                }
            }
            else
            {
                //	Apply event-function to element
            //	fvalidate.addEvent( elem, fv.config.clearEvent, fv.revertError, false );
                addEvent( elem, f.fv.config.clearEvent, f.fv, 'revertError', false );
            }
        }
        
        //	Set formatted name, current element
        if ( elem.attributes[f.fv.config.displayName] != null)
        {
            elem.fName = elem.attributes[f.fv.config.displayName].value.format();
        }
        else
        {
            elem.fName = elem.name.format();	
        }
        
        f.fv.elem		= elem;
        f.fv.type		= type;

        //	Create function to call the proper validator method of the fValidate class
        var func = new Function( "obj", "method", "obj[method]( " + params.toArgString() + " );" );
        func( f.fv, type );
    
        //	If element test failed AND group error is off, return false
        if ( elem.validated == false && groupError == false ) return false;
        
        //	Clear error if field okay
        if ( elem.validated == true ) f.fv.revertError();
    }
} //	end of element loop

//	If group error, show it
if ( groupError ) f.fv.showGroupError();

//	Return false if errors found
if ( f.fv.errors.length > 0 ) return false;

//	Show pre-submission confirmation
if ( bConfirm && !confirm( f.fv.config.confirmMsg ) )
{
    if ( f.fv.config.confirmAbortMsg != '' ) alert( f.fv.config.confirmAbortMsg );
    return false;
}

//	Disable reset and/or submit buttons if requested
if ( bDisable ) 
{
    if ( typeof f.fv.config.submitButton == 'object' )
    {
        var sb, j = 0;
        while( sb = f.fv.config.submitButton[j++] )
        {
            if ( f.fv.elementExists( sb ) )
            {
                f.elements[sb].disabled = true;
            }
        }
    }
    else if ( f.fv.elementExists( f.fv.config.submitButton ) )
    {
        f.elements[f.fv.config.submitButton].disabled = true;
    }
}
if ( bDisableR && f.fv.elementExists( f.fv.config.resetButton ) )
{
    f.elements[f.fv.config.resetButton].disabled = true;
}

//	Successful Validation.  Submit form
return true;

function addEvent( elem, evt, obj, method, capture )
{
    var self = elem;
    if ( typeof elem.attachEvent != 'undefined' )
    {
        elem.attachEvent( "on" + evt, function() { obj[method]( self ) } );
    }
    else if ( typeof elem.addEventListener != 'undefined' )
    {
        elem.addEventListener( evt, function() { obj[method]( self ) }, capture );
    }
    else if ( f.fv.config.eventOverride )
    {
        eleme['on' + evt] = function() { obj[method]( self ) };
    }
}
}

/*	Constructor
------------------------------------------- */
function fValidate( f, errorMode, groupError )
{
var self        = this;
this.form       = f;
this.errorMode  = errorMode;
this.groupError = groupError;
this.errors     = new Array();
this.validated  = true;
this.config     = new fValConfig();
this.i18n		= fvalidate.i18n;

//	Add reset action to clear visual error cues
f.onreset = function()
{
    var elem, i = 0;
    while ( elem = this.elements[i++] )
    {
        self.revertError( elem );
    }
}

addLabelProperties();

//	Parses form and adds label properties to elements that have one specified
function addLabelProperties()
{
    //	Collect all label elements in form, init vars		
    if ( typeof f.getElementsByTagName == 'undefined' ) return;
    var labels = f.getElementsByTagName( "label" );
    var label, i = j = 0;
    var elem;

    //	Loop through labels retrieved
    while ( label = labels[i++] )
    {
        //	For Opera 6
        if ( typeof label.htmlFor == 'undefined' ) return;
        
        //	Retrieve element
        elem = f.elements[label.htmlFor];
        if ( typeof elem == 'undefined' )
        {	//	No element found for label				
            self.devError( [label.htmlFor], 'noLabel' );
        }
        else if ( typeof elem.label != 'undefined' )
        {	//	label property already added
            continue;
        }
        else if ( typeof elem.length != 'undefined' && elem.length > 1 && elem.nodeName != 'SELECT' )
        {	//	For arrayed elements
            for ( j = 0; j < elem.length; j++ )
            {
                elem.item( j ).label = label;
            }
        }
        //	Regular label
        elem.label = label;
    }
}		
}

/*	Reset for another validation
------------------------------------------- */
fValidate.prototype._reset = function()
{
this.errors		= new Array();
this.showErrors	= new Array();
}

/*	Checks if element exists in form
------------------------------------------- */
fValidate.prototype.elementExists = function( elemName )
{
return Boolean( typeof this.form.elements[elemName] != 'undefined' );
}

/*	Receives error message and determines action
------------------------------------------- */
fValidate.prototype.throwError = function( args, which )
{
var elem  = this.elem;

//	Arrayed element?
if ( typeof elem.name == 'undefined' )
{
    elem = elem[0];
}

//	Bok requested AND element blank OR conditional validation?
if ( elem.bok && this.isBlank() )
{	//	skip		
    elem.validated = true;
    return;
}

//	Part of a conditional validation?
if ( elem.cv )
{
    return;
}

//	Set failsafe to false	
elem.validated = false;

//	Create error message
which	= this.setArg( which, 0 );
args	= this.setArg( args, [] );
emsgElem = ( typeof this.elem.getAttribute == "undefined" ) ?
        this.elem[0]:
        this.elem;
if ( emsgElem.getAttribute( this.config.emsg ) )
{
    var error = emsgElem.getAttribute( this.config.emsg );
}
var error = this.translateMessage( args, this.i18n.errors[this.type][which] );

//	Group error mode?
if ( this.groupError )
{
    //	Push error onto stack
    this.errors.push( {'elem':elem, 'msg': error} );		
}
else
{
    //	Process error message		
    this.showError( error, false, emsgElem );

    var focusElem = ( typeof elem.fields != 'undefined' )?
        elem.fields[0]:
        elem;
    
    //	Focus and select elements, if possible
    this.selectFocus( focusElem );
}
}


/*	Shows error message to user
------------------------------------------- */
fValidate.prototype.showError = function( emsg, last, elem )
{
//	Set variables
var self		= this,
    elem		= this.setArg( elem, this.elem ),
    isHidden	= Boolean( elem.type == 'hidden' ),
    label		= ( isHidden ) ? null : elem.label || null,
    emsg		= ( elem.getAttribute( this.config.emsg ) ) ? elem.getAttribute( this.config.emsg ).replace( /\\n/g, "\n" ) : emsg,
    errorClass	= this.config.errorClass,
    singleCSS	= this.config.useSingleClassNames;

if ( typeof this.showErrors == 'undefined' ) this.showErrors = new Array();	

//	Determine which error modes to use
switch( this.errorMode )
{	//	This represents all possible combinations
    case 0  : alertError(); break;
    case 1  : inputError(); break;
    case 2  : labelError(); break;
    case 3  : appendError(); break;
    case 4  : boxError(); break;
    case 5  : inputError(); labelError(); break;
    case 6  : inputError(); appendError(); break;
    case 7  : inputError(); boxError(); break;
    case 8  : inputError(); alertError(); break;
    case 9  : labelError(); appendError(); break;
    case 10 : labelError(); boxError(); break;
    case 11 : labelError(); alertError(); break;
    case 12 : appendError(); boxError(); break;
    case 13 : appendError(); alertError(); break;
    case 14 : boxError(); alertError(); break;
    case 15 : inputError(); labelError(); appendError(); break;
    case 16 : inputError(); labelError(); boxError(); break;
    case 17 : inputError(); labelError(); alertError(); break;
    case 18 : inputError(); appendError(); boxError(); break;
    case 19 : inputError(); appendError(); alertError(); break;
    case 20 : inputError(); boxError(); alertError(); break;
    case 21 : labelError(); appendError(); boxError(); break;
    case 22 : labelError(); appendError(); alertError(); break;
    case 23 : appendError(); boxError(); alertError(); break;
    case 24 : inputError(); labelError(); appendError(); boxError(); break;
    case 25 : inputError(); labelError(); appendError(); alertError(); break;
    case 26 : inputError(); appendError(); boxError(); alertError(); break;
    case 27 : labelError(); appendError(); boxError(); alertError(); break;
    case 28 : inputError(); labelError(); appendError(); boxError(); alertError(); break;		
}
//	Regular alert error
function alertError()
{
    if ( self.groupError ) self.showErrors.push( emsg );
    else alert( emsg );
    if ( last ) alert( self.i18n.groupAlert + self.showErrors.join( "\n\n- " ) );			
}
//	Applies class to form element
function inputError()
{
    if ( ( typeof elem.length != 'undefined' && elem.length > 1 && elem.nodeName != 'SELECT' ) || isHidden )
    {
        var subelem, i = 0;
        while( subelem = ( isHidden ) ? elem.fields[i++] : elem.item( i++ ) )			
        {
            if ( subelem.className != '' && singleCSS )
            {
                subelem.revertClass = subelem.className;
                subelem.className = errorClass;
            } else {
                self.addCSSClass( subelem, errorClass );
            }				
        }
    }
    else
    {
        if ( singleCSS )
        {
            elem.revertClass = elem.className;
            elem.className = errorClass;
        } else {
            self.addCSSClass( elem, errorClass );
        }
    }
}
//	Applies class to element's label
function labelError()
{
    if ( label == null ) return;
    if ( self.config.useSingleClassNames )
    {
        label.className = errorClass;
    } else {
        self.addCSSClass( label, errorClass );
    }
    
}
//	Appends error message to element's label
function appendError()
{
    if ( label == null || typeof label.innerHTML == 'undefined' ) return;
    if ( typeof label.original == 'undefined' )
        label.original = label.innerHTML;
    label.innerHTML = label.original + " - " + emsg.toHTML();
}
//	Appends Error message to pre-defined element
function boxError()
{
    if ( typeof self.boxError == 'undefined' ) self.boxError = document.getElementById( self.config.boxError );
    if ( self.boxError == null )
    {			
        self.devError( [self.config.boxError], 'noBox' );
        return;
    }
    if ( typeof self.elem.name == 'undefined' || self.elem.name == "" )
    {
        self.devError( [self.elem[self.config.code]], 'missingName' );
        return;
    }
    var errorId = self.config.boxErrorPrefix + self.elem.name,
        errorElem;
    if ( errorElem = document.getElementById( errorId ) ) // short-circuit
    {
        errorElem.firstChild.nodeValue = emsg.toHTML();
    }
    else
    {
        errorElem = document.createHTMLElement( 'li', { id: errorId, 'innerHTML': emsg.toHTML(), title: self.i18n.boxToolTip } );
        self.boxError.appendChild( errorElem );
        errorElem.onclick = function()
        {
            var elem = self.form.elements[this.id.replace( self.config.boxErrorPrefix, "" )];
            if ( typeof elem.fields != 'undefined' ) elem = elem.fields[0];
            if ( typeof elem.select != 'undefined' ) elem.select();
            if ( typeof elem.focus != 'undefined' ) elem.focus();
        }
    }
    self.boxError.style.display = "block";
}
}

/*	Handles element className manipulation
------------------------------------------- */
fValidate.prototype.removeCSSClass = function( elem, className )
{
elem.className = elem.className.replace( className, "" ).trim();
}
fValidate.prototype.addCSSClass = function( elem, className )
{
this.removeCSSClass( elem, className );
elem.className = ( elem.className + " " + className ).trim();
}

/*	Processes errors in stack for group error mode
------------------------------------------- */
fValidate.prototype.showGroupError = function()
{
for ( var error, firstElem, i = 0; ( error = this.errors[i] ); i++ )
{
    if ( i == 0 ) firstElem = error.elem;
    this.elem = error.elem;
    this.showError( error.msg, Boolean( i == ( this.errors.length - 1 ) ) );
}
var focusElem = ( typeof firstElem.fields != 'undefined' )?
    firstElem.fields[0]:
    firstElem;
this.selectFocus( focusElem );
}

/*	Reverts any visible error notification upon event
------------------------------------------- */
fValidate.prototype.revertError = function( elem )
{
elem = this.setArg( elem, this.elem );
var isHidden	= Boolean( elem.type == 'hidden' ),
    errorClass	= this.config.errorClass,
    i			= 0,
    errorElem,
    subelem;

if ( ( typeof elem.length != 'undefined' && elem.length > 1 && elem.nodeName != 'SELECT' ) || isHidden )
{
    if ( isHidden && typeof elem.fields != 'undefined' )
    {		
        while( subelem = ( isHidden ) ? elem.fields[i++] : elem.item( i++ ) )		
        {
            if ( typeof subelem.revertClass != 'undefined' )
            {
                subelem.className = subelem.revertClass;
            }
        }
    }
} else {
    if ( this.config.useSingleClassNames )
    {
        if ( typeof subElement.revertClass != 'undefined' )
        {
            elem.className = elem.revertClass;
        }
    } else {
        this.removeCSSClass( elem, errorClass );
    }		
}
if ( typeof elem.label != 'undefined' )
{
    if ( this.config.useSingleClassNames )
    {
        elem.label.className = '';
    } else {
        this.removeCSSClass( elem.label, errorClass );
    }
    elem.label.innerHTML = ( elem.label.original || elem.label.innerHTML );
}
if ( typeof this.boxError != 'undefined' )
{
    if ( typeof this.boxError.normalize != 'undefined' ) this.boxError.normalize();
    if ( errorElem = document.getElementById( this.config.boxErrorPrefix + elem.name ) )
    {
        this.boxError.removeChild( errorElem );
    }
    if ( this.boxError.childNodes.length == 0 ) this.boxError.style.display = "none";
}
}

/*	Focus and select elements, if possible
------------------------------------------- */
fValidate.prototype.selectFocus = function( elem )
{
if ( typeof elem.select != 'undefined' ) elem.select();
if ( typeof elem.focus != 'undefined' )  elem.focus();
}

/*	Developer assistance method - shows error if validator/element-type mismatch
------------------------------------------- */
fValidate.prototype.typeMismatch = function()
{
var pats = {
    'text':		'text|password|textarea',
    'ta':		'textarea',
    'hidden':	'hidden',
    's1':		'select-one',
    'sm':		'select-multiple',
    'select':	'select-one|select-multiple',
    'rg':		'radio',
    'radio':	'radio',
    'cb':		'checkbox',
    'file':		'file'
    };
var fail		= false,
    expected	= new Array(),
    result = key = type = regex = "";
for ( var i = 0; i < arguments.length; i++ )
{
    type	= pats[arguments[i]];
    regex	= new RegExp( type );
    result	+= ( regex.test( this.elem.type ) ) ? "1" : "0";
    key		+= "0";
    expected.push( type );		
}
if ( key ^ result == 0 )
{
    this.devError( [this.elem.fName, this.elem.type, expected.join( "|" ).replace( /\|/g, this.i18n.or )], 'mismatch' );
    this.elem.validated = false;
    return true;
}
return false;
}

/*	Returns value(s) of reference element passed
------------------------------------------- */
fValidate.prototype.getValue = function( elem )
{
switch ( elem.type )
{
    case 'text' :
    case 'password' :
    case 'textarea' :
    case 'hidden' :
    case 'file' :
        return elem.value;
    case 'radio':
    case 'select-single':
        if ( typeof elem.length == 'undefined' )
        {
            return elem.value;
        } else {
            for ( var i = 0; i < elem.length; i++ )
            {
                choice = ( elem.type == 'radio' ) ? "checked" : "selected";
                if ( elem[i][choice] )
                {
                    return elem[i].value;
                }
            }
        }
    case 'select-multiple' :
    case 'checkbox' :
        if ( typeof elem.length == 'undefined' )
        {
            return elem.value
        } else {
            var returnValues = new Array();
            for ( var i = 0; i < elem.length; i++ )
            {
                choice = ( elem.type == 'checkbox' ) ? "checked" : "selected";
                if ( elem[i][choice] )
                {
                    returnValues.push( elem[i].value );
                }
            }
            return returnValues;
        }
    default: return null;
}
}

/*	Generic argument setting method
------------------------------------------- */
fValidate.prototype.setArg = function( arg, def )
{
return ( typeof arg == 'undefined' || arg == '' || arg == null ) ? def : arg;
}

/*	Blank checker.  Optional string argument for evaluating element other than current
------------------------------------------- */
fValidate.prototype.isBlank = function( el )
{
var elem = this.form.elements[el] || this.elem;
return Boolean( /^\s*$/.test( elem.value ) );
}

/*	Translates messages using language file
------------------------------------------- */
fValidate.prototype.translateMessage = function( args, format )
{
var msg		= ""
for ( var i = 0; i < format.length; i++ )
{			
        msg += ( typeof format[i] == 'number' ) ? args[format[i]] : format[i];
}
return msg;
}

/*	Throws developer errors
------------------------------------------- */
fValidate.prototype.devError = function( args, which )
{
if ( typeof args == 'string' )
{
    which = args;
    args = [];
}
which = this.setArg( which, this.type );
var format = this.i18n.devErrors[which];
var a = [
    this.i18n.devErrors.lines[0],
    '----------------------------------------------------------------------------------------------',
    this.translateMessage( args, format ),
    '----------------------------------------------------------------------------------------------',
    this.i18n.devErrors.lines[1]
    ];
alert( a.join( "\n" ) );
}

/*	Throws specific developer error
------------------------------------------- */
fValidate.prototype.paramError = function( param, elemName )
{
elemName = this.setArg( elemName, this.elem.name );
this.devError( [param, this.type, elemName], 'paramError' );
}
/* Non-fValidate methods *****************************************/

/*	For easy creation of DOM nodes
------------------------------------------- */
document.createHTMLElement = function( elemName, attribs )
{
if ( typeof document.createElement == 'undefined' ) return;
var elem = document.createElement( elemName );
if ( typeof attribs != 'undefined' )
{
    for ( var i in attribs )
    {
        switch ( true )
        {
            case ( i == 'text' )  : elem.appendChild( document.createTextNode( attribs[i] ) ); break;
            case ( i == 'class' ) : elem.className = attribs[i]; break;
            default : elem.setAttribute( i, '' ); elem[i] = attribs[i];
        }
    }
}
return elem;    
}

/*	Trims b items from the beginning of the array, e items from the end
------------------------------------------- */
Array.prototype.reduce = function( b, e )
{
var a = new Array();
var count = 0;
for ( var i = b; i < this.length - e; i++ )
{
    a[count++] = this[i];
}
return a;
}

/*	Returns array as argument-compatible string
------------------------------------------- */
Array.prototype.toArgString = function()
{
var a = new Array();
for ( var i = 0; i < this.length; i++ )
{
    a.push( "'" + this[i] + "'" );
}	
return a.toString();
}

/*	Prototype push if missing
------------------------------------------- */
if ( typeof Array.push == 'undefined' )
Array.prototype.push = function()
{
var arg, i = 0;
while( arg = arguments[i++] )
{
    this[this.length] = arg;
}
return this.length;
}

/*	Returns last item of the array
------------------------------------------- */
Array.prototype.last = function()
{
return this[this.length-1];
}

/*	Removes the follow charaters _[] from an elements name for human-reading
------------------------------------------- */
String.prototype.format = function()
{
return this.replace( /\_/g, " ").replace( /\[|\]/g, "" );
}

/*	Replaces newline characters with XHTML BR tags
------------------------------------------- */
String.prototype.toHTML = function()
{
return this.replace( /\n/g, "<br />" ).replace( /\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;" );
}

/*	Trims leading and trailing whitespace from string
------------------------------------------- */
String.prototype.trim = function()
{
return this.replace( /^\s+|\s+$/, "" );
}

/*	Escapes necessary charactes for string-generated regular expressions
------------------------------------------- */
String.prototype.toPattern = function()
{
return this.replace( /([\.\*\+\{\}\(\)\<\>\^\$\\])/g, "\\$1" );
}





/*< blank basic *******************************************************************/
fValidate.prototype.blank = function()
{
if ( this.typeMismatch( 'text' ) ) return;
if ( this.isBlank() )
{
    this.throwError( [this.elem.fName] );
}
}
/*/>*/
/*< number numbers *******************************************************************/
fValidate.prototype.number = function( type, lb, ub )
{
if ( this.typeMismatch( 'text' ) ) return;
var num  = ( type == 0 ) ? parseInt( this.elem.value, 10 ) : parseFloat( this.elem.value );
lb       = this.setArg( lb, 0 );
ub       = this.setArg( ub, Number.infinity );
if ( lb > ub )
{
    this.devError( [lb, ub, this.elem.name] );
    return;
}
var fail = Boolean( isNaN( num ) || num != this.elem.value );
if ( !fail )
{
    switch( true )
    {
        case ( lb != false && ub != false ) : fail = !Boolean( lb <= num && num <= ub ); break;
        case ( lb != false ) : fail = Boolean( num < lb ); break;
        case ( ub != false ) : fail = Boolean( num > ub ); break;
    }
}
if ( fail )
{
    this.throwError( [this.elem.fName] );
    return;
}
this.elemPass = true;
}
/*/>*/
/*< numeric numbers *******************************************************************/
fValidate.prototype.numeric = function( len )
{
if ( this.typeMismatch( 'text' ) ) return;
len = this.setArg( len, '*' );
var regex = new RegExp( ( len == '*' ) ? "^\\d+$" : "^\\d{" + parseInt( len, 10 ) + "}\\d*$" );
if ( !regex.test( this.elem.value ) )
{
    if ( len == "*" )
    {
        this.throwError( [this.elem.fName] );
    } else {
        this.throwError( [len, this.elem.fName], 1 );
    }
}
}
/*/>*/
/*< length basic *******************************************************************/
fValidate.prototype.length = function( len, maxLen )
{
if ( this.typeMismatch( 'text' ) ) return;
var vlen = this.elem.value.length;
len		= Math.abs( len );
maxLen	= Math.abs( this.setArg( maxLen, Number.infinity ) );
if ( len > maxLen )
{
    this.devError( [len, maxLen, this.elem.name] );
    return;
}
if ( len > parseInt( vlen, 10 ) )
{
    this.throwError( [this.elem.fName, len] );
}	
if ( vlen > maxLen )
{
    this.throwError( [this.elem.fName, maxLen, vlen], 1 );
}
}
/*/>*/
/*< alnum extended *******************************************************************/
fValidate.prototype.alnum = function( minLen, tCase, numbers, spaces, puncs )
{
if ( this.typeMismatch( 'text' ) ) return;

tCase = this.setArg( tCase, "a" );

//alert( [minLen,tCase,numbers,spaces,puncs] );

numbers = ( numbers == "true" || numbers == "1" );
spaces = ( spaces == "true" || spaces == "1" );

//alert( [minLen,tCase,numbers,spaces,puncs] );
    
var okChars = "",
    arrE	= ['None','Any','No','No','Any'];

if ( minLen != '*' )
{
    minLen =  parseInt( minLen, 10 );
    arrE[0] = minLen;
} else {
    minLen = 0;
}

switch( tCase.toUpperCase() )
{
    case 'U':
        okChars += 'A-Z';
        arrE[1] =  'UPPER';
        break;
    case 'L':
        okChars += 'a-z';
        arrE[1] =  'lower';
        break;
    case 'C':
        okChars += 'A-Z][a-z';
        arrE[1] =  'Intial capital';
        minLen--;
        break;
    default:
        okChars += 'a-zA-Z';
        break;		
}

if ( numbers == true )
{
    okChars += '0-9';
    arrE[2] =  'Yes';
}
if ( spaces == true )
{
    okChars += ' ';
    arrE[3] =  'Yes';
}
if ( puncs == "any" )
{
    arrE[4]  = "Any";
}
else if ( puncs == "none" )
{
    arrE[4] = "None";
}
else 
{
    puncs = puncs.replace( /pipe/g, "|" );
    okChars += puncs;
    arrE[4] =  puncs; //.toPattern().replace( /\\/g, "" );
}
var length = ( minLen != "*" )?
    "{" + minLen + ",}":
    "+";
var regex = ( puncs == "any" ) ?
    new RegExp( "^([" + okChars + "]|[^a-zA-Z0-9\\s])" + length + "$" ):
    new RegExp( "^[" + okChars + "]" + length + "$" );

if ( !regex.test( this.elem.value ) )
{
    this.throwError( [this.elem.value, this.elem.fName, arrE[0], arrE[1], arrE[2], arrE[3], arrE[4]] );
}
}
/*/>*/
/*< equalto logical *******************************************************************/
fValidate.prototype.equalto = function( oName )
{
if ( this.typeMismatch( 'text' ) ) return;
if ( typeof oName == 'undefined' )
{
    this.paramError( 'oName' );
}
var otherElem = this.form.elements[oName];
if ( this.elem.value != otherElem.value )
{
    this.throwError( [this.elem.fName,otherElem.fName] );			
}
}
/*/>*/
/*< ssn extended *******************************************************************/
fValidate.prototype.ssn = function()
{
if ( this.typeMismatch( 'text' ) ) return;
if ( !( /^\d{3}\-\d{2}\-\d{4}$/.test( this.elem.value ) ) )
    this.throwError();
}
/*/>*/
/*< select controls *******************************************************************/
fValidate.prototype.select = function()
{
if ( this.typeMismatch( 's1' ) ) return;
if ( this.elem.selectedIndex == 0 )
{
    this.throwError( [this.elem.fName] );
}
}
/*/>*/
/*< selectm controls *******************************************************************/
fValidate.prototype.selectm = function( minS, maxS )
{
if ( this.typeMismatch( 'sm' ) ) return;
if ( typeof minS == 'undefined' )
{
    this.paramError( 'minS' );
}
if ( maxS == 999 || maxS == '*' || typeof maxS == 'undefined' || maxS > this.elem.length ) maxS = this.elem.length;

var count = 0;	
for ( var opt, i = 0; ( opt = this.elem.options[i] ); i++ )
{
    if ( opt.selected ) count++;
}

if ( count < minS || count > maxS )
{
    this.throwError( [minS, maxS, this.elem.fName, count] );
}
}
/*/>*/
/*< selecti controls *******************************************************************/
fValidate.prototype.selecti = function( indexes )
{

if ( this.typeMismatch( 's1' ) ) return;
if ( typeof indexes == 'undefined' )
{
    this.paramError( 'indexes' );
    return;
}
indexes = indexes.split( "," );
var selectOK = true;

for ( var i = 0; i < indexes.length; i++ )
{
    if ( this.elem.options[indexes[i]].selected )
    {
        selectOK = false;
        break;
    }
}
if ( !selectOK )
{
    this.throwError( [this.elem.fName] );
}
}
/*/>*/
/*< cazip international *******************************************************************/
fValidate.prototype.cazip = function()
{
var elem = this.elem;
if ( this.typeMismatch( 'text' ) ) return;
elem.value = elem.value.toUpperCase();
if ( !( /^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$/.test( elem.value ) ) )
{
    this.throwError();
}
}
fValidate.prototype.capost = fValidate.prototype.cazip;
/*/>*/
/*< ukpost international *******************************************************************/
fValidate.prototype.ukpost = function()
{
var elem = this.elem;
if ( this.typeMismatch( 'text' ) ) return;
elem.value = elem.value.toUpperCase();
if ( !( /^[A-Z]{1,2}\d[\dA-Z] ?\d[A-Z]{2}$/.test( elem.value ) ) )
{
    this.throwError();
}
}
/*/>*/
/*< germanpost international *******************************************************************/
fValidate.prototype.germanpost = function()
{
var elem = this.elem;
if ( this.typeMismatch( 'text' ) ) return;
elem.value = elem.value.toUpperCase();
if ( !( /^(?:CH\-)\d{4}$/.test( elem.value ) ) )
{
    this.throwError();
}
}
/*/>*/
/*< swisspost international *******************************************************************/
fValidate.prototype.swisspost = function()
{
var elem = this.elem;
if ( this.typeMismatch( 'text' ) ) return;
elem.value = elem.value.toUpperCase();
if ( !( /^(?:D\-)\d{5}$/.test( this.elem.value ) ) )
{
    this.throwError();
}
}
/*/>*/
/*< email web *******************************************************************/
fValidate.prototype.email = function( level )
{
if ( this.typeMismatch( 'text' ) ) return;
if ( typeof level == 'undefined' ) level = 0;
var emailPatterns = [
    /.+@.+\..+$/i,
    /^\w.+@\w.+\.[a-z]+$/i,
    /^\w[-_a-z~.]+@\w[-_a-z~.]+\.[a-z]{2}[a-z]*$/i,
    /^\w[\w\d]+(\.[\w\d]+)*@\w[\w\d]+(\.[\w\d]+)*\.[a-z]{2,7}$/i
    ];
if ( ! emailPatterns[level].test( this.elem.value ) )
{
    this.throwError();
}	
}	
/*/>*/
/*< url web *******************************************************************/
fValidate.prototype.url = function( hosts, hostOptional, allowQS )
{
if ( this.typeMismatch( 'text' ) ) return;

this.setArg( hosts, "http" );

var front = "^(?:(" + hosts.replace( /\,/g, "|" ) + ")\\:\\/\\/)";
var end   = ( Boolean( allowQS ) == true ) ? "(\\?.*)?$" : "$";

if ( Boolean( hostOptional ) == true ) front += "?";
var regex = new RegExp( front + "([\\w\\d-]+\\.?)+" + end );

if ( !regex.test( this.elem.value ) )
{
    this.throwError( [this.elem.fName] );
}
}	
/*/>*/
/*< ip web *******************************************************************/
fValidate.prototype.ip = function( portMin, portMax )
{
if ( this.typeMismatch( 'text' ) ) return;
portMin = this.setArg( portMin, 0 );
portMax = this.setArg( portMax, 99999 );
if ( !( /^\d{1,3}(\.\d{1,3}){3}(:\d+)?$/.test( this.elem.value ) ) )
{
    this.throwError();
}
else
{
    var part, i = 0, parts = this.elem.value.split( /[.:]/ );
    while ( part = parts[i++] )
    {
        if ( i == 5 ) // Check port
        {
            if ( part < portMin || part > portMax )
            {
                this.throwError( [part, portMin, portMax], 1 );
            }
        }
        else if ( part < 0 || part > 255 )
        {
            this.throwError();
        }
    }
}
}
/*/>*/
/*< decimal numbers *******************************************************************/
fValidate.prototype.decimal = function( lval, rval )
{
if ( this.typeMismatch( 'text' ) ) return;
var regex = '', elem = this.elem;
if ( lval != '*' ) lval = parseInt( lval, 10 );
if ( rval != '*' ) rval = parseInt( rval, 10 );

if ( lval == 0 )
    regex = "^\\.[0-9]{" + rval + "}$";	
else if ( lval == '*' )
    regex = "^[0-9]*\\.[0-9]{" + rval + "}$";
else if ( rval == '*' )
    regex = "^[0-9]{" + lval + "}\\.[0-9]+$";
else
    regex = "^[0-9]{" + lval + "}\\.[0-9]{" + rval + "}$";
    
regex = new RegExp( regex );

if ( !regex.test( elem.value ) )
{
    this.throwError( [elem.value,elem.fName] );
}	
}
/*/>*/
/*< decimalr numbers *******************************************************************/
fValidate.prototype.decimalr = function( lmin, lmax, rmin, rmax )
{
if ( this.typeMismatch( 'text' ) ) return;
lmin = ( lmin == '*' )? 0 : parseInt( lmin, 10 );
lmax = ( lmax == '*' )? '': parseInt( lmax, 10 );
rmin = ( rmin == '*' )? 0 : parseInt( rmin, 10 );
rmax = ( rmax == '*' )? '': parseInt( rmax, 10 );
var	decReg = "^[0-9]{"+lmin+","+lmax+"}\\.[0-9]{"+rmin+","+rmax+"}$"
var regex = new RegExp(decReg);
if ( !regex.test( this.elem.value ) )
{
    this.throwError( [this.elem.fName] );
}
return true;
}
/*/>*/
/*< zip extended *******************************************************************/
fValidate.prototype.zip = function( sep )
{
if ( this.typeMismatch( 'text' ) ) return;
sep = this.setArg( sep, "- " );
var regex = new RegExp( "^[0-9]{5}(|[" + sep.toPattern() + "][0-9]{4})?$" );
if ( ! regex.test( this.elem.value ) )
{
    this.throwError();
}
}
/*/>*/
/*< phone extended *******************************************************************/
fValidate.prototype.phone = function( format )
{
if ( this.typeMismatch( 'text' ) ) return;
format       = this.setArg( format, 0 );
var patterns = [
    /^(\(?\d\d\d\)?)?[ -]?\d\d\d[ -]?\d\d\d\d$/,	//	loose
    /^(\(\d\d\d\) )?\d\d\d[ -]\d\d\d\d$/			//	strict
    ];
if ( !patterns[format].test( this.elem.value ) )
{
    if ( format == 1 )
    {
        this.throwError();
    } else {
        this.throwError( [], 1 );
    }
}
}
/*/>*/
/*< date datetime *******************************************************************/
fValidate.prototype.date = function( formatStr, delim, code, specDate )
{
if ( this.typeMismatch( 'text' ) ) return;
if ( typeof formatStr == 'undefined' )
{
    this.paramError( 'formatStr' );
    return;
}

delim = this.setArg( delim, "/" );

var error	= [this.elem.fName, formatStr.replace( /\//g, delim )];
var format  = formatStr.split( "/" );
var compare = this.elem.value.split( delim );
var order   = new Object();

for ( var i = 0; i < format.length; i++ )
{
    switch( format[i].charAt( 0 ).toLowerCase() )
    {
        case 'm' :
            order.months = i;
            break;
        case 'd' :
            order.days = i;
            break;
        case 'y' :
            order.years = i;
            break;
    }
}
var thisDate = new Date( compare[order.years], compare[order.months]-1, compare[order.days] );

if ( isNaN( thisDate ) || thisDate.getDate() != compare[order.days] || thisDate.getMonth() != compare[order.months]-1 || thisDate.getFullYear().toString().length != formatStr.match( /y/g ).length )
{
    this.throwError( error );
    return;
}

var compareElem = this.form.elements[specDate];
if ( typeof compareElem != 'undefined' )
{
    specDate = compareElem.validDate || compareElem.value;
}
var compareDate = ( specDate == 'today' )?
    new Date():
    new Date( specDate );
compareDate.setHours(0);
compareDate.setMinutes(0);
compareDate.setSeconds(0);
compareDate.setMilliseconds(0);

var timeDiff = compareDate.getTime() - thisDate.getTime();
var dateOk   = false;

switch ( parseInt( code ) ) {
    case 1 :	// Before specDate
        dateOk	= Boolean( timeDiff > 0 );
        error	= 1;
        break;
    case 2 :	// Before or on specDate
        dateOk	= Boolean( ( timeDiff + 86400000 ) > 0 );
        error	= 2;
        break;
    case 3 :	// After specDate
        dateOk	= Boolean( timeDiff < 0 );
        error	= 3;
        break;
    case 4 :	// After or on specDate
        dateOk	= Boolean( ( timeDiff - 86400000 ) < 0 );
        error	= 4;
        break;
    default : dateOk = true;
    }
if ( !dateOk )
{
    this.throwError( [specDate], error );
}
this.elem.validDate = thisDate.toString();
}	
/*/>*/
/*< money ecommerce *******************************************************************/
fValidate.prototype.money = function( ds, grp, dml )
{
if ( this.typeMismatch( 'text' ) ) return;

ds  = ( ds == ' ' )  ? false : ds.toPattern();
grp = ( grp == ' ' ) ? false : grp.toPattern();
dml = ( dml == ' ' ) ? false : dml.toPattern();

var moneySyntax, pattern;

switch( true )
{
    case Boolean( ds && grp && dml ):		// Dollar sign, grouping, and decimal
        pattern		= "^" + ds + "(?:(?:[0-9]{1,3}" + grp + ")(?:[0-9]{3}" + grp + ")*[0-9]{3}|[0-9]{1,3})(" + dml + "[0-9]{2})$";
        moneySyntax = ds + "XX" + grp + "XXX" + dml + "XX";
        break;
    case Boolean( ds && grp && !dml ):		// Dollar sign and grouping
        pattern		= "^" + ds + "(?:(?:[0-9]{1,3}" + grp + ")(?:[0-9]{3}" + grp + ")*[0-9]{3}|[0-9]{1,3})$";
        moneySyntax = "" + ds + "XX" + grp + "XXX";
        break;
    case Boolean( ds && !grp && dml ):		// Dollar sign and decimal
        pattern		="^" + ds + "[0-9]*(\\.[0-9]{2})$";
        moneySyntax ="" + ds + "XXXXX" + dml + "XX";
        break;
    case Boolean( !ds && grp && dml ):		// Grouping and decimal
        pattern		="^(?:(?:[0-9]{1,3}" + grp + ")(?:[0-9]{3}" + grp + ")*[0-9]{3}|[0-9]{1,3})(" + dml + "[0-9]{2})?$";
        moneySyntax ="XX" + grp + "XXX" + dml + "XX";
        break;
    case Boolean( ds && !grp && !dml ):		// Dollar sign only
        pattern		="^" + ds + "[0-9]*$";
        moneySyntax ="" + ds + "XXXXX";
        break;
    case Boolean( !ds && grp && !dml ):		// Grouping only
        pattern		="^(?:(?:[0-9]{1,3}" + grp + ")(?:[0-9]{3}" + grp + ")*[0-9]{3}|[0-9]{1,3})$";
        moneySyntax ="XX" + grp + "XXX";
        break;
    case Boolean( !ds && !grp && dml ):		// Decimal only
        pattern		="^[0-9]*(" + dml + "[0-9]{2})$";
        moneySyntax ="XXXXX" + dml + "XX";
        break;
    case Boolean( !ds && !grp && !dml ):	// No params set, all special chars become optional
        pattern		="^.?(?:(?:[0-9]{1,3}.?)(?:[0-9]{3}.?)*[0-9]{3}|[0-9]{1,3})(.[0-9]{2})?$";
        moneySyntax ="[?]XX[?]XXX[?XX]";
}
        
var regex = new RegExp( pattern );
if ( !regex.test( this.elem.value ) )
{
    this.throwError( [this.elem.fName, moneySyntax.replace( /\\/g, '' )] );
}
}
/*/>*/
/*< checkbox controls *******************************************************************/
fValidate.prototype.checkbox = function( minC, maxC )
{
if ( this.typeMismatch( 'cb' ) ) return;
if ( typeof minC == 'undefined' )
{
    this.paramError( 'minC' );
    return;
}
if ( this.elem == this.form.elements[this.elem.name] && !this.elem.checked )
{
    this.throwError( [this.elem.fName] );
}
else
{
    this.elem = this.form.elements[this.elem.name];
    var len   = this.elem.length;
    var count = 0;
    
    if ( maxC == 999 || maxC == '*' || typeof maxC == 'undefined' || maxC > this.elem.length )
    {
        maxC == len;
    }
    var i = len;
    while( i-- > 0 )
    {
        if ( this.elem[i].checked )
        {
            count++;
        }
    }
    if ( count < minC || count > maxC )
    {
        this.throwError( [minC, maxC, this.elem[0].fName, count] );
    }			
}
}
/*/>*/
/*< radio controls *******************************************************************/
fValidate.prototype.radio = function()
{
if ( this.typeMismatch( 'rg' ) ) return;
if ( this.elem == this.form.elements[this.elem.name] && !this.elem.checked )
{
    this.throwError( [this.elem.fName] );
}
else
{
    this.elem = this.form.elements[this.elem.name];
    
    for ( var i = 0; i < this.elem.length; i++ )
    {
        if ( this.elem.item( i ).checked )
        {
            return;
        }
    }
    this.throwError( [this.elem[0].fName] );
}
}
/*/>*/
/*< eitheror logical *******************************************************************/
fValidate.prototype.eitheror = function()
{
if ( this.typeMismatch( 'hidden' ) ) return;
if ( typeof arguments[0] == 'undefined' )
{
    this.paramError( 'delim' );
    return;
}
if ( typeof arguments[1] == 'undefined' )
{
    this.paramError( 'fields' );
    return;
}
var arg, i  = 0,
    fields  = new Array(),
    field,
    nbCount = 0,		
    args    = arguments[1].split( arguments[0] );		

this.elem.fields = new Array();

while ( arg = args[i++] )
{
    field = this.form.elements[arg];
    fields.push( field.fName );
    this.elem.fields.push( field );

    if ( !this.isBlank( arg ) )
    {
        nbCount++;
    }
}
if ( nbCount != 1 )
{
    this.throwError( [fields.join( "\n\t-" )] );
}
}
/*/>*/
/*< atleast logical *******************************************************************/
fValidate.prototype.atleast = function()
{
if ( this.typeMismatch( 'hidden' ) ) return;
if ( typeof arguments[0] == undefined )
{
    this.paramError( 'qty' );
    return;
}
if ( typeof arguments[1] == undefined )
{
    this.paramError( 'delim' );
    return;
}
if ( typeof arguments[2] == undefined )
{
    this.paramError( 'fields' );
    return;
}
var arg, i  = 0,
    fields  = new Array(),
    field,
    nbCount = 0,
    args    = arguments[2].split( arguments[1] );

this.elem.fields = new Array();

while ( arg = args[i++] )
{
    field = this.form.elements[arg];
    fields.push( field.fName );
    this.elem.fields.push( field );

    if ( !this.isBlank( arg ) )
    {
        nbCount++;
    }
}
if ( nbCount < arguments[0] )
{
    this.throwError( [arguments[0], fields.join( "\n\t-" ), nbCount] );
}
}
/*/>*/
/*< allornone logical *******************************************************************/
fValidate.prototype.allornone = function()
{
if ( this.typeMismatch( 'hidden' ) ) return;
if ( typeof arguments[0] == 'undefined' )
{
    this.paramError( 'delim' );
    return;
}
if ( typeof arguments[1] == 'undefined' )
{
    this.paramError( 'fields' );
    return;
}
var arg, i  = 0,
    fields  = new Array(),
    field,
    nbCount = 0,
    args    = arguments[1].split( arguments[0] );

this.elem.fields = new Array();

while ( arg = args[i++] )
{
    field = this.form.elements[arg];
    fields.push( field.fName );
    this.elem.fields.push( field );

    if ( !this.isBlank( arg ) )
    {
        nbCount++;
    }
}
if ( nbCount > 0 && nbCount < args.length )
{
    this.throwError( [fields.join( "\n\t-" ), nbCount] );
}
}
/*/>*/
/*< comparison logical *******************************************************************/
fValidate.prototype.comparison = function( field1, operator, field2 )
{
if ( this.typeMismatch( 'hidden' ) ) return;
var elem1	= this.form.elements[field1],
    elem2	= this.form.elements[field2],
    value1	= this.getValue( elem1 ),
    value2	= this.getValue( elem2 );
    i18n	= this.i18n.comparison;
    i		= -1;

var operators =
[
    ['>',	i18n.gt],
    ['<',	i18n.lt],
    ['>=',	i18n.gte],
    ['<=',	i18n.lte],
    ['==',	i18n.eq],
    ['!=',	i18n.neq]
];
while( operators[++i][0] != operator ){ }
this.elem.fields = [elem1, elem2];
if ( ! eval( value1 + operator + value2 ) )
{
    this.throwError( [elem1.fName, operators[i][1], elem2.fName] );
}
}
/*/>*/
/*< file controls *******************************************************************/
fValidate.prototype.file = function( extensions, cSens )
{
if ( this.typeMismatch( 'file' ) ) return;
if ( typeof extensions == 'undefined' )
{
    this.paramError( 'extensions' );
    return;
}
cSens = Boolean( cSens ) ? "" : "i";
var regex = new RegExp( "^.+\\.(" + extensions.replace( /,/g, "|" ) + ")$", cSens );
if ( ! regex.test( this.elem.value ) )
{
    this.throwError( [extensions.replace( /,/g, "\n" )] );
}
}
/*/>*/
/*< custom special *******************************************************************/
fValidate.prototype.custom = function( flags, reverseTest )
{
if ( this.typeMismatch( 'text' ) ) return;
flags     = ( flags ) ? flags.replace( /[^gim]/ig ) : "";
var regex = new RegExp( this.elem.getAttribute( this.config.pattern ), flags );
if ( !regex.test( this.elem.value ) )
{
    this.throwError( [this.elem.fName] );
}	
}
/*/>*/
/*< cc ecommerce *******************************************************************/
fValidate.prototype.cc = function()
{
if ( this.typeMismatch( 'text' ) ) return;
var typeElem = this.form.elements[this.config.ccType];

if ( !typeElem )
{
    this.devError( 'noCCType' )
    return;
}
var ccType   = typeElem.options[typeElem.selectedIndex].value.toUpperCase();

var types    = {
    'VISA'    : /^4\d{12}(\d{3})?$/,
    'MC'      : /^5[1-5]\d{14}$/,
    'DISC'    : /^6011\d{12}$/,
    'AMEX'    : /^3[4|7]\d{13}$/,        
    'DINERS'  : /^3[0|6|8]\d{12}$/,
    'ENROUTE' : /^2[014|149]\d{11}$/,
    'JCB'     : /^3[088|096|112|158|337|528]\d{12}$/,
    'SWITCH'  : /^(49030[2-9]|49033[5-9]|49110[1-2]|4911(7[4-9]|8[1-2])|4936[0-9]{2}|564182|6333[0-4][0-9]|6759[0-9]{2})\d{10}(\d{2,3})?$/,
    'DELTA'   : /^4(1373[3-7]|462[0-9]{2}|5397[8|9]|54313|5443[2-5]|54742|567(2[5-9]|3[0-9]|4[0-5])|658[3-7][0-9]|659(0[1-9]|[1-4][0-9]|50)|844[09|10]|909[6-7][0-9]|9218[1|2]|98824)\d{10}$/,
    'SOLO'    : /^(6334[5-9][0-9]|6767[0-9]{2})\d{10}(\d{2,3})?$/
    };
if ( typeElem.validated == false && this.groupError == true ) return;
if ( typeof types[ccType] == 'undefined' && typeElem.validated == false && this.groupError == false )
{
    this.devError( [ccType] );
    return;
}
this.elem.value = this.elem.value.replace( /[^\d]/g, "" );
if ( !types[ccType].test( this.elem.value ) || !this.elem.value.luhn() )
{
    this.throwError( [this.elem.fName] );
}
}


String.prototype.luhn = function()
{
var i = this.length;
var checkSum = "", digit;
while ( digit = this.charAt( --i ) )
{
    checkSum += ( i % 2 == 0 ) ? digit * 2 : digit;
}
checkSum = eval( checkSum.split('').join('+') );
return ( checkSum % 10 == 0 );
}
/*/>*/
/*< ccDate ecommerce *******************************************************************/
fValidate.prototype.ccDate = function( month, year )
{
if ( this.typeMismatch( 's1' ) ) return;
year	= parseInt( this.getValue( this.form.elements[year] ), 10 ) + 2000;
month	= parseInt( this.getValue( this.form.elements[month] ), 10 );

var today	= new Date();
var expDate = new Date( year, month )

if ( expDate < today )
{
    alert( ["Card Expired",today,expDate].join( "\n" ) );
}
}
/*/>*/











/*--	fValidate US-English language file.
*
*	Translation by: Peter Bailey
*	Email: me@peterbailey.net
*
*	Visit http://www.peterbailey.net/fValidate/api/i18n/
*	for additional translations and instructions on
*	making your own translation.
*
*	!!! WARNING !!! Changing anything but the literal 
*	strings will likely cause script failure!
*
*	Note: This document most easily read/edited with tab-
*	spacing set to 4
*
*********************************************************/

if ( typeof fvalidate == 'undefined' )
{
var fvalidate = new Object();
}

fvalidate.i18n =
{
//	Validation errors
errors:
{
    blank:		[
        ["Please enter ", 0]
        ],
    length:		[
        [0, " must be at least ", 1, " characters long"],
        [0, " must be no more than ", 1, " characters long.\nThe current text is ", 2, " characters long."]
        ],
    equalto:	[
        [0, " must be equal to ", 1]
        ],
    number:		[
        ["The number you entered for ", 0, " is not valid"]
        ],
    numeric:	[
        ["Only numeric values are valid for the ", 0],
        ["A minimum of ", 0, " numeric values are required for the ", 1]
        ],
    alnum:		[
        ["The data you entered, \"", 0, "\", does not match the requested format for ", 1,  
        "\nMinimum Length: ", 2,
        "\nCase: ", 3,
        "\nNumbers allowed: ", 4,
        "\nSpaces allowed: ", 5,
        "\nPunctuation characters allowed: ", 6, "\n"]
        ],
    decimal:	[
        ["The data you entered,", 0, " is not valid.  Please re-enter the ", 1]
        ],
    decimalr:	[
        [0, " is not a valid. Please re-enter."]
        ],
    ip:			[
        ["Please enter a valid IP"],
        ["The port number you specified, ", 0, ",  is out of range.\nIt must be between ", 1, " and ", 2]
        ],
    ssn:		[
        ["You need to enter a valid Social Security Number.\nYour SSN must be entered in 'XXX-XX-XXXX' format."]
        ],
    money:		[
        [0, " does not match the required format of ", 1]
        ],
    cc:			[
        ["The ", 0, " you entered is not valid. Please check again and re-enter."]
        ],
    ccDate:		[
        ["You credit card has expired! Please use a different card."]
        ],
    zip:		[
        ["Please enter a valid 5 or 9 digit Zip code."]
        ],
    phone:		[
        ["Please enter a valid phone number plus Area Code."],
        ["Please enter a valid phone number - seven or ten digits."]
        ],
    email:		[
        ["Please enter a valid email address"]
        ],
    url:		[
        [0, " is not a valid domain"]
        ],
    date:		[
        ["The data entered for ", 0, " is not a valid date\nPlease enter a date using the following format: ", 1],
        ["Date must be before ", 0],
        ["Date must be on or before ", 0],
        ["Date must be after ", 0],
        ["Date must be on or after ", 0]
        ],
    select:		[
        ["Please select a valid option for ", 0]
        ],
    selectm:	[
        ["Please select between ", 0, " and ", 1, " options for ", 2, ".\nYou currently have ", 3, " selected"]
        ],
    selecti:	[
        ["Please select a valid option for ", 0]
        ],
    checkbox:	[
        ["Please check ", 0, " before continuing"],
        ["Please select between ", 0, " and ", 1, " options for ", 2, ".\nYou currently have ", 3, " selected"]
        ],
    radio:		[
        ["Please check ", 0, " before continuing"],
        ["Please select an option for ", 0 ]
        ],
    comparison:	[
        [0, " must be ", 1, " ", 2]
        ],
    eitheror:	[
        ["One and only one of the following fields must be entered:\n\t-", 0, "\n"]
        ],
    atleast:	[
        ["At least ", 0, " of the following fields must be entered:\n\t-", 1, "\n\nYou have only ", 2, " filled in.\n"]
        ],
    allornone:	[
        ["All or none of the following fields must be entered and accurate:\n\t-", 0, "\nYou have only ", 1, " accurate field entered.\n"]
        ],
    file:		[
        ["The file must be one of the following types:\n", 0, "\nNote: File extension may be case-sensitive."]
        ],
    custom:		[
        [0, " is invalid."]
        ],
    cazip:		[
        ["Please enter a valid postal code."]
        ],
    ukpost:		[
        ["Please enter a valid postcode."]
        ],
    germanpost:	[
        ["Please enter a valid postcode."]
        ],
    swisspost:	[
        ["Please enter a valid postcode."]
        ]
},

comparison:
{
    gt:		"greater than",
    lt:		"less than",
    gte:	"greater than or equal to",
    lte:	"less than or equal to",
    eq:		"equal to",
    neq:	"not equal to"
},

//	Developer assist errors
devErrors:
{
    number:		["The lower-bound (", 0, ") is greater than the upper-bound (", 1, ") on this element: ", 2],
    length:		["The minimum length (", 0, ") is greater than the maxiumum legnth (", 1, ") on this element: ", 2],
    cc:			["Credit Card type (", 0, ") not found."],

    lines:		["! WARNING ! -- fValidate developer-assist error\n", "\nIf you are not the developer, please contact the website administrator regarding this error."],
    paramError: ["You must include the '", 0, "' parameter for the '", 1, "' validator type on this field: ", 2],
    notFound:	["The validator '", 0, "' was not found.\nRequested by: ", 1],
    noLabel:	["No element found for label: ", 0],
    noBox:		["An element with the requested id '", 0, "' was not found for the 'boxError' config value."],
    missingName:["The hidden input calling the following logical validator must have a valid name\nattribute when used in conjunction with the 'box' error-type.\n\t", 0],
    mismatch:	["Validator/Element type mismatch.\n\nElement: ", 0, "\nElement type: ", 1, "\nType required by validator: ", 2],
    noCCType:	["You must include a SELECT item with Credit Card type choices!"]
},

//	Config values
config :
{
    confirmMsg :		"Your data is about to be sent.\nPlease click 'Ok' to proceed or 'Cancel' to abort.",
    confirmAbortMsg :	"Submission cancelled.  Data has not been sent."
},

//	Tooltip attached to Box-item errors
boxToolTip:	"Click to target field",

//	Message displayed at top of alert error in group mode
groupAlert:	"The following errors occured:\n\n- ",

//	Literal translation of the English 'or', include padding spaces.
or:			" or "
}




window.onerror = null;
var topMargin = 100;
var slideTime = 1200;
var ns6 = (!document.all && document.getElementById);
var ie4 = (document.all);
var ns4 = (document.layers);
function layerObject(id,left) {
if (ns6) {
this.obj = document.getElementById(id).style;
this.obj.left = left;
return this.obj;
}
else if(ie4) {
this.obj = document.all[id].style;
this.obj.left = left;
return this.obj;
}
else if(ns4) {
this.obj = document.layers[id];
this.obj.left = left;
return this.obj;
   }
}
function layerSetup() {
floatLyr = new layerObject('floatLayer', 0);
window.setInterval("main()", 10)
}
function floatObject() {
if (ns4 || ns6) {
findHt = window.innerHeight;
} else if(ie4) {
findHt = document.body.clientHeight;
   }
} 
function main() {
if (ns4) {
this.currentY = document.layers["floatLayer"].top;
this.scrollTop = window.pageYOffset;
mainTrigger();
}
else if(ns6) {
this.currentY = parseInt(document.getElementById('floatLayer').style.top);
this.scrollTop = scrollY;
mainTrigger();
} else if(ie4) {
this.currentY = floatLayer.style.pixelTop;
this.scrollTop = document.body.scrollTop;
mainTrigger();
   }
}
function mainTrigger() {
var newTargetY = this.scrollTop + this.topMargin;
if ( this.currentY != newTargetY ) {
if ( newTargetY != this.targetY ) {
this.targetY = newTargetY;
floatStart();
}
animator();
   }
}
function floatStart() {
var now = new Date();
this.A = this.targetY - this.currentY;
this.B = Math.PI / ( 2 * this.slideTime );
this.C = now.getTime();
if (Math.abs(this.A) > this.findHt) {
this.D = this.A > 0 ? this.targetY - this.findHt : this.targetY + this.findHt;
this.A = this.A > 0 ? this.findHt : -this.findHt;
}
else {
this.D = this.currentY;
   }
}
function animator() {
var now = new Date();
var newY = this.A * Math.sin( this.B * ( now.getTime() - this.C ) ) + this.D;
newY = Math.round(newY);
if (( this.A > 0 && newY > this.currentY ) || ( this.A < 0 && newY < this.currentY )) {
if ( ie4 )document.all.floatLayer.style.pixelTop = newY;
if ( ns4 )document.layers["floatLayer"].top = newY;
if ( ns6 )document.getElementById('floatLayer').style.top = newY + "px";
   }
}

function start_persistent_div() {
    if(ns6||ns4) {
        pageWidth = innerWidth;
        pageHeight = innerHeight;
        layerSetup();
        floatObject();
    }
    else if(ie4) {
        pageWidth = document.body.clientWidth;
        pageHeight = document.body.clientHeight;
        layerSetup();
    floatObject();
   }
}

