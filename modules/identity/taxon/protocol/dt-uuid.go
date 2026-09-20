/* For license and copyright information please see the LEGAL file in the code repository */

package taxon_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_TaxonID interface {
	TaxonID() UUID
}

type UUID record_p.UUID
