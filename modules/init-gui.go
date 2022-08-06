// go:build gui

/* For license and copyright information please see LEGAL file in repository */

package modules

import (
	qd "github.com/GeniusesGroup/organization/modules/quiddity-domain"
)

// Init method use to register all available modules to the application.
func Init() {
	qd.RegisterServices() 
	qd.RegisterPages() 
	qd.RegisterWidgets()
}
