import _ from 'lodash'
import React from 'react'
import { Search, Input } from 'semantic-ui-react'

const initialState = { isLoading: false, results: [], value: '' }

const getResults = () =>
  _.times(5, () => ({
    title: "koksowo",
    description: "Fajne koksy",
    image: '',
    price: '110',
  }))

const source = _.range(0, 3).reduce((memo) => {
  const name = "jo"

  // eslint-disable-next-line no-param-reassign
  memo[name] = {
    name,
    results: getResults(),
  }

  return memo
}, {})

export default class SearchExampleCategory extends React.Component {
  state = initialState

  handleResultSelect = (e, { result }) => this.setState({ value: result.title })

  handleSearchChange = (e, { value }) => {
    this.setState({ isLoading: true, value })

    setTimeout(() => {
      if (this.state.value.length < 1) return this.setState(initialState)

      const re = new RegExp(_.escapeRegExp(this.state.value), 'i')
      const isMatch = (result) => re.test(result.title)

      const filteredResults = _.reduce(
        source,
        (memo, data, name) => {
          const results = _.filter(data.results, isMatch)
          if (results.length) memo[name] = { name, results } // eslint-disable-line no-param-reassign

          return memo
        },
        {},
      )

      this.setState({
        isLoading: false,
        results: filteredResults,
      })
    }, 300)
  }

  render() {
    const { isLoading, value, results } = this.state

    return (
        <Search
        input={
          <Input
            transparent={true}//this.props.transparent}
            className='icon'
            icon='search' 
            placeholder='Search...'
            inverted={this.props.transparent}
          />
        }
        category
        loading={isLoading}
        onResultSelect={this.handleResultSelect}
        onSearchChange={_.debounce(this.handleSearchChange, 500, {
            leading: true,
        })}
        results={results}
        value={value}
        className=''
        />
        
    )
  }
}