import React from 'react';

import PropTypes from 'prop-types';

import Typography from '@material-ui/core/Typography';

export default function PageHeader({ title }) {
  return (
    <Typography
      component="h2"
      variant="h4"
      color="textPrimary"
      style={{ marginBottom: '20px' }}
    >
      {title}
    </Typography>
  );
}

PageHeader.propTypes = {
  title: PropTypes.string.isRequired,
};

PageHeader.defaultProps = {
  title: '',
};
