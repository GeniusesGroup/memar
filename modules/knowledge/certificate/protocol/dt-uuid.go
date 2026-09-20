/* For license and copyright information please see the LEGAL file in the code repository */

package ecp

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_CertificateID interface {
	CertificateID() UUID
}

type UUID thing_p.UUID
