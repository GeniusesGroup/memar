/* For license and copyright information please see the LEGAL file in the code repository */

package node

import (
	er "memar/error"
)

// Errors
var (
	ErrNoNodeAvailable er.Error
	// ErrContentAlreadyExist     er.Error
	// ErrCantPrepareStatement    er.Error
	// ErrStoringDataNotComplete  er.Error
	// ErrDatabaseConnectionError er.Error
	// ErrDatabasePingOut         er.Error
)

func init() {
	ErrNoNodeAvailable.Init("domain/memar.scm.geniuses.group; package=node; type=error; name=no-node-available")

	// ErrContentAlreadyExist    .Init("This content was already exist")
	// ErrCantPrepareStatement   .Init("Can't prepare a new statement to database")
	// ErrStoringDataNotComplete .Init("We have some problem in storing your data in our databases. Send your request again! If error exist contact software administrators")
	// ErrDatabaseConnectionError.Init("Could not connect to database")
	// ErrDatabasePingOut        .Init("Error occurred in Ping to database")
}
