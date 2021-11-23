import React from 'react';
import renderer from 'react-test-renderer';
import Dendrogram from '../../pages/Dendrogram/Dendrogram';

describe('Test Login Page', () => {
  it('Renders login page correctly', () => {
    const imgString =
      'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==';
    const tree = renderer.create(<Dendrogram imgString={imgString}/>).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
