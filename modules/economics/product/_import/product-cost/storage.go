/* For license and copyright information please see the LEGAL file in the code repository */

package pc

import (
	"crypto/sha512"

	"libgo/ganjine"
	"libgo/log"
	"libgo/math"
	"libgo/pehrest"
	"libgo/price"
	"libgo/syllab"
)

const (
	productCostStructureID uint64 = 2759922966933000947
)

var productCostStructure = ds.DataStructure{
	ID:                 2759922966933000947,
	IssueDate:          1607422485,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "", // Other structure name
	ExpireInFavorOfID:  0,  // Other StructureID! Handy ID or Hash of ExpireInFavorOf!
	Status:             ds.DataStructureStatePreAlpha,
	Structure:          ProductCost{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Product Cost",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"",
	},
}

// ProductCost ---Read locale description in productCostStructure---
type ProductCost struct {
	OrgID      [32]byte // Sell can be register just by producer organization
	QuiddityID [32]byte `index-hash:"RecordID"`

	MaterialsPercent   math.PerMyriad
	MaterialsCost      price.Amount
	LaborPercent       math.PerMyriad
	LaborCost          price.Amount
	InvestmentsPercent math.PerMyriad
	InvestmentsCost    price.Amount
	TotalCost          price.Amount

	Markup          math.PerMyriad // the % added to the cost to determine the wholesale price
	WholesaleProfit price.Amount   // The amount of wholesale markup
	Margin          math.PerMyriad // the % of product price to determine the retail price
	RetailProfit    price.Amount   // The amount of retail margin

	Cost price.Amount

	TaxPercent math.PerMyriad // VAT, ...
	Tax        price.Amount
}

// SaveNew method set some data and write entire ProductCost record with all indexes!
func (pp *ProductCost) SaveNew() (err protocol.Error) {
	err = pp.Set()
	if err != nil {
		return
	}
	pp.IndexRecordIDForQuiddityID()
	return
}

// Update method set some data and write entire ProductCost record with needed indexes!
func (pp *ProductCost) Update() (err protocol.Error) {
	err = pp.SaveNew()
	return
}

// Set method set some data and write entire ProductCost record!
func (pp *ProductCost) Set() (err protocol.Error) {
	pp.RecordStructureID = productCostStructureID
	pp.RecordSize = pp.LenAsSyllab()
	pp.WriteTime = etime.Now()
	pp.OwnerAppID = protocol.App.Manifest().AppUUID()

	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: pp.ToSyllab(),
	}
	pp.RecordID = sha512.Sum512_256(req.Record[32:])
	copy(req.Record[0:], pp.RecordID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		if protocol.AppDebugMode {
			log.Debug("Ganjine - Set Record Error:", err)
		}
		// TODO::: Handle error situation
	}

	return
}

// GetByRecordID read existing record data by given RecordID!
func (pp *ProductCost) GetByRecordID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		RecordID:          pp.RecordID,
		RecordStructureID: productCostStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = pp.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if pp.RecordStructureID != productCostStructureID {
		log.Warn("Platform collapsed!! HASH Collision Occurred on", productCostStructureID)
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByQuiddityID method read last existing record data by given QuiddityID!
func (pp *ProductCost) GetLastByQuiddityID() (err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pp.hashQuiddityIDForRecordID(),
		Offset:   18446744073709551615,
		Limit:    1,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	if err != nil {
		return
	}

	pp.RecordID = indexRes.IndexValues[0]
	err = pp.GetByRecordID()
	if err.Equal(ganjine.ErrMisMatchedStructureID) {
		log.Warn("Platform collapsed!! HASH Collision Occurred on", productAuctionStructureID)
	}
	return
}

/*
	-- Search Methods --
*/

// FindRecordsIDsByQuiddityID find RecordsIDs by given ID
func (pp *ProductCost) FindRecordsIDsByQuiddityID(offset, limit uint64) (RecordsIDs [][32]byte, err protocol.Error) {
	var indexRequest = &pehrest.HashGetValuesReq{
		IndexKey: pp.hashQuiddityIDForRecordID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexRequest)
	RecordsIDs = indexRes.IndexValues
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexRecordIDForQuiddityID save RecordID chain for QuiddityID
// Call in each update to the exiting record!
func (pp *ProductCost) IndexRecordIDForQuiddityID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pp.hashQuiddityIDForRecordID(),
		IndexValue: pp.RecordID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.AppDebugMode {
			log.Debug("Ganjine - Set Index Error:", err)
		}
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pp *ProductCost) hashQuiddityIDForRecordID() (hash [32]byte) {
	const field = "QuiddityID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productCostStructureID)
	copy(buf[8:], pp.QuiddityID[:])
	copy(buf[40:], field)
	return sha512.Sum512_256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// ??

/*
	-- LIST FIELDS --
*/

// ??

/*
	-- Temporary INDEXES & LIST --
*/

// ??

/*
	-- Syllab Encoder & Decoder --
*/

func (pp *ProductCost) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < pp.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(pp.RecordID[:], buf[0:])
	pp.RecordStructureID = syllab.GetUInt64(buf, 32)
	pp.RecordSize = syllab.GetUInt64(buf, 40)
	pp.WriteTime = etime.Time(syllab.GetInt64(buf, 48))
	copy(pp.OwnerAppID[:], buf[56:])

	copy(pp.AppInstanceID[:], buf[88:])
	copy(pp.UserConnectionID[:], buf[120:])
	copy(pp.OrgID[:], buf[152:])
	copy(pp.QuiddityID[:], buf[184:])

	pp.MaterialsPercent = math.PerMyriad(syllab.GetUInt16(buf, 216))
	pp.MaterialsCost = price.Amount(syllab.GetInt64(buf, 218))
	pp.LaborPercent = math.PerMyriad(syllab.GetUInt16(buf, 226))
	pp.LaborCost = price.Amount(syllab.GetInt64(buf, 228))
	pp.InvestmentsPercent = math.PerMyriad(syllab.GetUInt16(buf, 236))
	pp.InvestmentsCost = price.Amount(syllab.GetInt64(buf, 238))
	pp.TotalCost = price.Amount(syllab.GetInt64(buf, 246))

	pp.Markup = math.PerMyriad(syllab.GetUInt16(buf, 254))
	pp.WholesaleProfit = price.Amount(syllab.GetInt64(buf, 256))
	pp.Margin = math.PerMyriad(syllab.GetUInt16(buf, 264))
	pp.RetailProfit = price.Amount(syllab.GetInt64(buf, 266))

	pp.Cost = price.Amount(syllab.GetInt64(buf, 274))

	pp.TaxPercent = math.PerMyriad(syllab.GetUInt16(buf, 282))
	pp.Tax = price.Amount(syllab.GetInt64(buf, 284))
	return
}

func (pp *ProductCost) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	buf = make([]byte, pp.LenAsSyllab())

	copy(buf[0:], pp.RecordID[:])
	syllab.SetUInt64(buf, 32, pp.RecordStructureID)
	syllab.SetUInt64(buf, 40, pp.RecordSize)
	syllab.SetInt64(buf, 48, int64(pp.WriteTime))
	copy(buf[56:], pp.OwnerAppID[:])

	copy(buf[88:], pp.AppInstanceID[:])
	copy(buf[120:], pp.UserConnectionID[:])
	copy(buf[152:], pp.OrgID[:])
	copy(buf[184:], pp.QuiddityID[:])

	syllab.SetUInt16(buf, 216, uint16(pp.MaterialsPercent))
	syllab.SetInt64(buf, 218, int64(pp.MaterialsCost))
	syllab.SetUInt16(buf, 226, uint16(pp.LaborPercent))
	syllab.SetInt64(buf, 228, int64(pp.LaborCost))
	syllab.SetUInt16(buf, 236, uint16(pp.InvestmentsPercent))
	syllab.SetInt64(buf, 238, int64(pp.InvestmentsCost))
	syllab.SetInt64(buf, 246, int64(pp.TotalCost))

	syllab.SetUInt16(buf, 254, uint16(pp.Markup))
	syllab.SetInt64(buf, 256, int64(pp.WholesaleProfit))
	syllab.SetUInt16(buf, 264, uint16(pp.Margin))
	syllab.SetInt64(buf, 266, int64(pp.RetailProfit))

	syllab.SetInt64(buf, 274, int64(pp.Cost))

	syllab.SetUInt16(buf, 282, uint16(pp.TaxPercent))
	syllab.SetInt64(buf, 284, int64(pp.Tax))
	return
}

func (pp *ProductCost) LenOfSyllabStack() uint32 {
	return 292
}

func (pp *ProductCost) LenOfSyllabHeap() (ln uint32) {
	return
}

func (pp *ProductCost) LenAsSyllab() uint64 {
	return uint64(pp.LenOfSyllabStack() + pp.LenOfSyllabHeap())
}
