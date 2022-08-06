// go:build server

/* For license and copyright information please see LEGAL file in ChaparKhane repository */
// Auto-generated, edits will be overwritten

package modules

import (
	qd "github.com/GeniusesGroup/organization/modules/quiddity-domain"
)

// Init method use to register all available modules to the application.
func Init() {
	qd.RegisterServices()
}
