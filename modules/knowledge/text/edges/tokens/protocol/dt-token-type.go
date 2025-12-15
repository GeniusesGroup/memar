/* For license and copyright information please see the LEGAL file in the code repository */

package tokens_p

import label_p "org/modules/knowledge/label/protocol"

type Field_TokenType interface {
	TokenType() TokenType
}

type TokenType label_p.Field_LabelID
