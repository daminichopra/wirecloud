/*
*     (C) Copyright 2008 Telefonica Investigacion y Desarrollo
*     S.A.Unipersonal (Telefonica I+D)
*
*     This file is part of Morfeo EzWeb Platform.
*
*     Morfeo EzWeb Platform is free software: you can redistribute it and/or modify
*     it under the terms of the GNU Affero General Public License as published by
*     the Free Software Foundation, either version 3 of the License, or
*     (at your option) any later version.
*
*     Morfeo EzWeb Platform is distributed in the hope that it will be useful,
*     but WITHOUT ANY WARRANTY; without even the implied warranty of
*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*     GNU Affero General Public License for more details.
*
*     You should have received a copy of the GNU Affero General Public License
*     along with Morfeo EzWeb Platform.  If not, see <http://www.gnu.org/licenses/>.
*
*     Info about members and contributors of the MORFEO project
*     is available at
*
*     http://morfeo-project.org
 */

// This class represents the parameter that a filter can have
function Param (name_, label_, type_, index_, required_, defaultValue_){
    this._name = name_;
    this._label = label_;
    this._type = type_;
    this._index = index_;
    this._required = !!required_;
    this._defaultValue = defaultValue_;
}

Param.prototype.Param = function (name_, label_, type_, index_, required_, defaultValue_){
    this._name = name_;
    this._label = label_;
    this._type = type_;
    this._index = index_;
    this._required = !!required_;
    this._defaultValue = defaultValue_;
}

Param.prototype.getName = function() {
    return this._name;
}

Param.prototype.getType = function() {
    return this._type;
}

Param.prototype.getLabel = function() {
    return this._label;
}

Param.prototype.getIndex = function() {
    return this._index;
}

Param.prototype.getRequired = function() {
    return this._required;
}

Param.prototype.getDefaultValue = function() {
    return this._defaultValue;
}


/**********************************************************************************************************/
Param.prototype.validate = function(value) {
    var current_pattern, current_modifiers,interger_value, jpath_exp;
    if(!value){
        if(this.getRequired()){
            throw Error (gettext("Look out! a value for '%(paramName)s' is required"));
        }
    }
    // Checks the type of parameter
    switch (this.getType()){
    case 'N': // Param is Number
        interger_value = Number(value);
        if (isNaN(interger_value)){
            throw Error (gettext("Error loading parameter '%(paramName)s'. It must be a number"));
        }
        break;
    case 'regexp': // Param is RegExp
        if ((value.indexOf('/') == 0) && (value.lastIndexOf('/') > 0)){
            current_pattern = value.substring(1, value.lastIndexOf('/'));
            current_modifiers = value.substring(value.lastIndexOf('/') + 1, value.length);
            //This new RegExp launch exceptions if the ER have any problem.
            new RegExp(current_pattern, current_modifiers);
        }else {
            new RegExp (value);
        }
        break;
    //Carlos: Revisar si es necesario el .parse y el ,replace.
    case 'jpath': // Param is a JPATH expresion (for JSON)
        jpath_exp = this.parse(value);
        break;
    default: // Otherwise is String
        value.replace(/"/g,"'");
        break;
    }
};
/**********************************************************************************************************/

/**
 * @class
 *
 * Description of a filter. Has information about the parameters this filter.
 */
function Filter (id_, name_, label_, nature_, code_, category_, params_, helpText_) {
  this._id = id_;
  this._name = name_;
  this._label = label_;
  this._nature = nature_;
  this._params = new Array();
  this._lastExecError = null;
  this._category = category_;
  this._helpText = helpText_;

  // Sets the filter parameters
  this.processParams (params_);

  // Sets the filter code
  try{
     eval ('this._code = ' + code_);

     if ((typeof this._code) != 'function')
        this._code = null;

  }catch(e){
    this._code = null;

    var msg = interpolate(gettext("Error loading code of the filter '%(filterName)s'."), {filterName: this._label}, true);
    LogManagerFactory.getInstance().log(msg, Constants.ERROR_MSG);
  }
}

Filter.prototype.getNature = function() {
  return this._nature;
}

Filter.prototype.getId = function() {
  return this._id;
}

Filter.prototype.getName = function() {
  return this._name;
}

Filter.prototype.getLabel = function() {
  return this._label;
}

Filter.prototype.getParams = function() {
  return this._params;
}

Filter.prototype.getlastExecError = function() {
  return this._lastExecError;
}

Filter.prototype.setParam = function(param_) {
  this._params[param_.getIndex()] = param_;
}

Filter.prototype.hasParams = function() {
  return this._params.length != 0;
}

Filter.prototype.getCategory = function() {
  return this._category;
}

Filter.prototype.getHelpText = function() {
  return this._helpText;
}

Filter.prototype.processParams = function(params_) {
  this._params = new Array();
  if (params_ != null && params_ != ''){
    var fParam, paramObject;
    var jsonParams = JSON.parse(params_);
    for (var i = 0; i < jsonParams.length; i++) {
        fParam = jsonParams[i];
        if (fParam.type == 'jpath'){
            paramObject = new JPathParam (fParam.name, fParam.label, fParam.index, fParam.required, fParam.defaultValue);
        } else {
            paramObject = new Param(fParam.name, fParam.label, fParam.type, fParam.index, fParam.required, fParam.defaultValue);
        }
        this.setParam(paramObject);
    }
  }
}

Filter.prototype.getInitialValues = function() {
    var params = {}, param;

    for (var i = 0; i < this._params.length; i++) {
        param = this._params[i];
        params[param._index] = this._params[i]._defaultValue;
    }

    return params;
}

Filter.prototype.run = function(channelValue_, paramValues_, channel) {
    var i, msg, params = {};

    // Begins to run, no errors
    this._lastExecError = null;

//  // Creates the varible for the channel value
//  eval ("var channelValue = '" + channelValue_ + "';");

    try{
        // Creates the variables for other params
        for (i=0; i < this._params.length; ++i){

            var paramValue = paramValues_[i];

            if(!paramValue){
                if(this._params[i].getRequired()){
                    msg = interpolate(gettext("Look out! '%(paramName)s' of '%(filterName)s' is required"),
                        {paramName: this._params[i].getLabel(), filterName: this._label}, true);
                    this._lastExecError = msg;
                    return gettext('undefined');

                }else{
                    params [this._params[i].getName()] = null;
                    continue;
                }
            }


            // Checks the type of parameter
            switch (this._params[i].getType()){
            case 'N': // Param is Number
                var interger_value = parseInt(paramValue);

                if (isNaN(interger_value)){
                    msg = interpolate(gettext("Error loading parameter '%(paramName)s' of the filter '%(filterName)s'. It must be a number"),
                        {paramName: this._params[i].getLabel(), filterName: this._label}, true);
                    LogManagerFactory.getInstance().log(msg, Constants.ERROR_MSG);
                    this._lastExecError = msg;
                    return gettext('undefined');
                }
                params[this._params[i].getName()] = paramValue;
                break;
            case 'regexp': // Param is RegExp
                if ((paramValue.indexOf('/') == 0) && (paramValue.lastIndexOf('/') > 0)){
                    var current_pattern = paramValue.substring(1, paramValue.lastIndexOf('/'));
                    var current_modifiers = paramValue.substring(paramValue.lastIndexOf('/') + 1, paramValue.length);
                    params[this._params[i].getName()] = new RegExp(current_pattern, current_modifiers);
                }else {
                    params[this._params[i].getName()] = new RegExp (paramValue);
                }
                break;
            case 'jpath': // Param is a JPATH expresion (for JSON)
                var jpath_exp = this._params[i].parse(paramValue);
                params[this._params[i].getName()] = this._params[i].parse(paramValue);
                break;
            default: // Otherwise is String
                params[this._params[i].getName()] = paramValue.replace(/"/g,"'");
                break;
            }


        }
    }catch(e){
        msg = interpolate(gettext("Error loading param '%(paramName)s' of the filter '%(filterName)s': %(error)s."),
            {paramName: this._params[i].getLabel(), filterName: this._label, error: e}, true);
        LogManagerFactory.getInstance().log(msg, Constants.ERROR_MSG);
        this._lastExecError = msg;
        return gettext('undefined');
    }

    try{

        // Executes the filter code
        return this._code(channelValue_, channel, params);

    }catch(err){
        if(err.name == "DONT_PROPAGATE"){
            throw new DontPropagateException(err)
        }
        else{
            var msg = interpolate(gettext("Error executing code of the filter '%(filterName)s'."), {filterName: this._Label}, true);
            LogManagerFactory.getInstance().log(msg, Constants.ERROR_MSG);
            // Saves the message (for wiring interface)
            if (this._params.length == 0){
                this._lastExecError = msg;
            }else{
                this._lastExecError = interpolate(gettext("Error executing code of the filter '%(filterName)s'. Check the parametres."), {filterName: this._label}, true);
            }
            return gettext('undefined');
        }
    }

}
