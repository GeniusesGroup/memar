/* For license and copyright information please see the LEGAL file in the code repository */

package clap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
)

// It can point to any domain records e.g. product, invoice, ...
// It can be use in other way than domain indicate e.g.
// - welcome message by group-associated domain data.
// - Map domain to share static or live location
// - PhotoUpdated
// - Call
// TODO::: prevent from flag set is on with other types like text

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	DomainID() protocol.MediaTypeID // use to detect comment GUI template
	// TODO::: primary key may not be a single field!
	RecordID() protocol.UUID // in above domain
	RecordVersion() uint64   // VersionOffset

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
