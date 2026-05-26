/* For license and copyright information please see the LEGAL file in the code repository */

package text_type_p

import label_p "org/modules/knowledge/label/protocol"

type Field_Type interface {
	TextType() Type
}

type Type label_p.Field_LabelID
