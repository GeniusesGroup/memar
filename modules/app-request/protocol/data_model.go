/* For license and copyright information please see the LEGAL file in the code repository */

package arp

import (
	aap "org/modules/app-audit/protocol"
	acp "org/modules/app-connection/protocol"
	app "org/modules/app-page/protocol"
	asp "org/modules/app-service/protocol"
	sp "org/modules/storage/protocol"
	up "org/modules/user/protocol"
)

// Application service request domain use to prove how other records created as a chain to other records or standalone data.

// DataModel indicates the domain record data fields.
type DataModel interface {
	aap.AuditRequest
	UserID() up.UserUUID              // TODO::: Duplicate with ConnectionID?? But need for index purpose!
	ConnectionID() acp.ConnectionUUID // Store to remember which request belongs to which Connection/AppInstance.
	ServiceID() asp.ServiceUUID       //
	PageID() app.PageUUID             // If request is from GUI applications.
	CompressID() uint64               // e.g. gzip
	RequestData() RequestData         // Decode by service request structure and compress type.

	sp.SaveTime
}
