/* For license and copyright information please see the LEGAL file in the code repository */

package modules

import (
	"memar/services"

	ggbuService "org/modules/chapar_khane/services/get-gp-by-user"
)

// RegisterServerServices method use to register all available modules to the application.
func RegisterServerServices() {
	services.Register(&ggbuService.Service)
	// s.Services.RegisterService()
	// s.Services.RegisterService()
}
