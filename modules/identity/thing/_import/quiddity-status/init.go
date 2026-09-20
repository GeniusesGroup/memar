/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/protocol"
)

// Init method use to register services and storage structure in the application.
func Init() {
	protocol.App.RegisterService(&registerQuiddityService)
	protocol.App.RegisterService(&registerQuiddityNewLanguageService)
	protocol.App.RegisterService(&updateQuiddityService)
	protocol.App.RegisterService(&getQuiddityService)
	protocol.App.RegisterService(&findQuiddityByTitleService)
	protocol.App.RegisterService(&findQuiddityByURIService)
	protocol.App.RegisterService(&FindQuiddityByOrgIDService)
	protocol.App.RegisterService(&getQuiddityLanguagesService)
	// protocol.App.RegisterService(&)

	protocol.OS.RegisterMediaType(&quiddityStructure)
}
