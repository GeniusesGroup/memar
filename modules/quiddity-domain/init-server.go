/* For license and copyright information please see LEGAL file in ChaparKhane repository */

package qd

import (
	"github.com/GeniusesGroup/libgo/protocol"

	qds "github.com/GeniusesGroup/organization/modules/quiddity-domain/services"
)

// RegisterServices will register services in the application.
func RegisterServices() {
	protocol.App.RegisterService(&qds.Register)
	protocol.App.RegisterService(&qds.Get)
}
