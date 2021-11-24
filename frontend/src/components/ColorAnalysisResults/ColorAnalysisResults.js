import React from 'react'

const ColorAnalysisResults = ({results}) => {
    return (
        <div>
            <div>RGB Values and Proportion</div>
            {results.colors.map((color, idx) => {
                return (
                <div key={idx} style={{
                    backgroundColor: `rgb(${color.red}, ${color.green}, ${color.blue})`,
                }}>
                    <span style={{padding: '0.5rem'}}>
                        <span style={{mixBlendMode: 'difference'}}>{color.red}, </span>
                        <span style={{mixBlendMode: 'difference'}}>{color.green}, </span>
                        <span style={{mixBlendMode: 'difference'}}>{color.blue}</span>
                    </span>
                    <span>
                        <span style={{float: 'right', mixBlendMode: 'difference'}}>{(color.proportion * 100).toFixed(3)}%</span>
                    </span>
                </div>
                )
            })}
        </div>
    )
}

export default ColorAnalysisResults
